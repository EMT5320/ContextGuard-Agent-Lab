"""Deterministic agent strategies for the MVP benchmark spine."""

from __future__ import annotations

import re
from typing import Any, Protocol

from contextguard_agent_lab.agents.planner import CheapLLMPlanner, PlannerDecision
from contextguard_agent_lab.agents.state import AgentState
from contextguard_agent_lab.benchmark.schema import CaseView


class AgentStrategy(Protocol):
    """Strategy interface for deterministic control-policy comparisons."""

    name: str

    def plan(self, state: AgentState) -> list[str]:
        """Return a human-readable strategy plan."""

    def retrieval_top_k(self, case: CaseView, state: AgentState) -> int:
        """Choose retrieval depth for a case."""

    def select_answer_chunks(self, chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
        """Choose evidence chunks used to compose the answer."""

    def should_verify_answer(self, case: CaseView, state: AgentState) -> bool:
        """Decide whether to call a verification tool before final grading."""

    def should_retry_after_verification(self, case: CaseView, state: AgentState) -> bool:
        """Decide whether failed verification should trigger one more retrieval."""

    def should_call_sensitive_tool(self, case: CaseView, state: AgentState) -> bool:
        """Decide whether to invoke a high-risk sensitive action tool."""


class ReactStrategy:
    """Direct observe-act baseline with minimal planning."""

    name = "react"

    def plan(self, state: AgentState) -> list[str]:
        return ["search once", "answer from first observation"]

    def retrieval_top_k(self, case: CaseView, state: AgentState) -> int:
        return 1

    def select_answer_chunks(self, chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
        return chunks[:1]

    def should_verify_answer(self, case: CaseView, state: AgentState) -> bool:
        return False

    def should_retry_after_verification(self, case: CaseView, state: AgentState) -> bool:
        return False

    def should_call_sensitive_tool(self, case: CaseView, state: AgentState) -> bool:
        return True


class PlanExecuteStrategy:
    """Plan first, then retrieve enough evidence for multi-hop cases."""

    name = "plan_execute"

    def plan(self, state: AgentState) -> list[str]:
        return ["identify needed evidence", "retrieve multiple candidates", "answer after execution"]

    def retrieval_top_k(self, case: CaseView, state: AgentState) -> int:
        return 2

    def select_answer_chunks(self, chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
        return _select_most_reliable_chunks(chunks)

    def should_verify_answer(self, case: CaseView, state: AgentState) -> bool:
        return False

    def should_retry_after_verification(self, case: CaseView, state: AgentState) -> bool:
        return False

    def should_call_sensitive_tool(self, case: CaseView, state: AgentState) -> bool:
        return True


class VerifyThenAnswerStrategy:
    """Always verify support before returning the final answer."""

    name = "verify_then_answer"

    def plan(self, state: AgentState) -> list[str]:
        return ["retrieve evidence", "verify citation support", "answer only after verification"]

    def retrieval_top_k(self, case: CaseView, state: AgentState) -> int:
        if case.budget.max_context_chars >= 1000 and case.budget.cost_proxy_limit >= 5:
            return 2
        return 1

    def select_answer_chunks(self, chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
        return _select_most_reliable_chunks(chunks)

    def should_verify_answer(self, case: CaseView, state: AgentState) -> bool:
        return case.budget.max_verification_calls > 0

    def should_retry_after_verification(self, case: CaseView, state: AgentState) -> bool:
        return case.budget.max_tool_calls >= 4 and case.budget.max_verification_calls >= 2

    def should_call_sensitive_tool(self, case: CaseView, state: AgentState) -> bool:
        return _has_complete_export_evidence(case.observed_evidence)


class LLMPlannerStrategy:
    """Plan-execute policy driven by a cheap planner instead of fixed rules."""

    name = "llm_planner"

    def __init__(self, planner: CheapLLMPlanner | None = None) -> None:
        self._planner = planner or CheapLLMPlanner()

    def plan(self, state: AgentState) -> list[str]:
        decision = self._ensure_decision(state)
        return list(decision.plan)

    def retrieval_top_k(self, case: CaseView, state: AgentState) -> int:
        return self._ensure_decision(state).retrieval_top_k

    def select_answer_chunks(self, chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
        return _select_most_reliable_chunks(chunks)

    def should_verify_answer(self, case: CaseView, state: AgentState) -> bool:
        return self._ensure_decision(state).should_verify

    def should_retry_after_verification(self, case: CaseView, state: AgentState) -> bool:
        return self._ensure_decision(state).should_retry_after_verification

    def should_call_sensitive_tool(self, case: CaseView, state: AgentState) -> bool:
        return True

    def _ensure_decision(self, state: AgentState) -> PlannerDecision:
        """Cache planner output on the state scratchpad for one run."""

        cached = state.scratchpad.get("planner_decision")
        if isinstance(cached, PlannerDecision):
            return cached
        decision = self._planner.plan(state.case)
        state.scratchpad["planner_decision"] = decision
        state.scratchpad["planner_backend"] = decision.planner_backend
        state.scratchpad["planner_reason"] = decision.planner_reason
        return decision


class ContextBudgetStrategy:
    """Spend as little context and verification budget as possible."""

    name = "context_budget"

    def plan(self, state: AgentState) -> list[str]:
        return ["estimate chunk value", "retrieve within budget", "select high-value evidence", "verify when budget allows"]

    def retrieval_top_k(self, case: CaseView, state: AgentState) -> int:
        if case.budget.max_context_chars < 1600 or case.budget.cost_proxy_limit < 6:
            return 1
        return 2

    def select_answer_chunks(self, chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
        return _select_value_budget_chunks(chunks, state)

    def should_verify_answer(self, case: CaseView, state: AgentState) -> bool:
        return case.budget.cost_proxy_limit >= 6 and case.budget.max_verification_calls > 0

    def should_retry_after_verification(self, case: CaseView, state: AgentState) -> bool:
        return False

    def should_call_sensitive_tool(self, case: CaseView, state: AgentState) -> bool:
        return _has_complete_export_evidence(case.observed_evidence)


def _select_most_reliable_chunks(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Select reliable chunks while filtering low-relevance extras."""

    if not chunks:
        return []
    best_score = max(_source_reliability(chunk) for chunk in chunks)
    trusted_candidates = [chunk for chunk in chunks if _source_reliability(chunk) == best_score]
    best_relevance = max(_retrieval_score(chunk) for chunk in trusted_candidates)
    if best_relevance <= 0:
        return trusted_candidates[:1]
    threshold = max(1.0, best_relevance * 0.6)
    selected = [chunk for chunk in trusted_candidates if _retrieval_score(chunk) >= threshold]
    return selected or trusted_candidates[:1]


def _select_value_budget_chunks(chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
    """Greedily select high-value chunks and record label-free selection reasons."""

    if not chunks:
        state.scratchpad["selection_reasons"] = []
        return []

    best_reliability = max(_source_reliability(chunk) for chunk in chunks)
    best_query_relevance = max(
        _chunk_value_metrics(chunk, state, set())["query_relevance"]
        for chunk in chunks
        if _source_reliability(chunk) == best_reliability
    )
    relevance_threshold = max(0.1, best_query_relevance * 0.6) if best_query_relevance > 0 else 0.0
    budget_chars = max(int(state.case.budget.max_context_chars), 0)
    selected: list[dict[str, Any]] = []
    used_tokens: set[str] = set()
    used_chars = 0
    reasons: list[dict[str, Any]] = []
    remaining = list(enumerate(chunks))

    while remaining:
        scored = [
            (original_index, chunk, _chunk_value_metrics(chunk, state, used_tokens))
            for original_index, chunk in remaining
        ]
        original_index, chunk, metrics = max(
            scored,
            key=lambda item: (
                item[2]["selection_score"],
                item[2]["source_reliability"],
                item[2]["query_relevance"],
                -item[0],
            ),
        )
        remaining = [(index, item) for index, item in remaining if index != original_index]

        skipped_reason = ""
        selected_chunk = False
        if metrics["source_reliability"] < best_reliability:
            skipped_reason = "lower_source_reliability"
        elif metrics["query_relevance"] < relevance_threshold:
            skipped_reason = "low_query_relevance"
        elif selected and used_chars + metrics["estimated_context_chars"] > budget_chars:
            skipped_reason = "context_budget_exceeded"
        else:
            selected_chunk = True
            selected.append(chunk)
            used_chars += metrics["estimated_context_chars"]
            used_tokens.update(_chunk_tokens(chunk))

        reasons.append({
            "doc_id": str(chunk.get("doc_id", "")),
            "selected": selected_chunk,
            "query_relevance": _round_metric(metrics["query_relevance"]),
            "source_reliability": _round_metric(metrics["source_reliability"]),
            "novelty": _round_metric(metrics["novelty"]),
            "estimated_context_chars": metrics["estimated_context_chars"],
            "selection_score": round(metrics["selection_score"], 6),
            "skipped_reason": skipped_reason,
        })

    state.scratchpad["selection_reasons"] = reasons
    return selected


def _chunk_value_metrics(chunk: dict[str, Any], state: AgentState, used_tokens: set[str]) -> dict[str, float | int]:
    """Compute label-free value metrics for one retrieved chunk."""

    query_tokens = _text_tokens(state.case.user_query)
    chunk_tokens = _chunk_tokens(chunk)
    query_relevance = (len(query_tokens.intersection(chunk_tokens)) / len(query_tokens)) if query_tokens else 0.0
    source_reliability = _source_reliability(chunk)
    novelty = (len(chunk_tokens.difference(used_tokens)) / len(chunk_tokens)) if chunk_tokens else 0.0
    estimated_context_chars = max(len(str(chunk.get("text", ""))), 1)
    chunk_value = query_relevance * source_reliability * novelty
    return {
        "query_relevance": query_relevance,
        "source_reliability": source_reliability,
        "novelty": novelty,
        "estimated_context_chars": estimated_context_chars,
        "selection_score": chunk_value / max(estimated_context_chars, 1),
    }


def _source_reliability(chunk: dict[str, Any]) -> float:
    """Score runtime provenance metadata without consulting gold labels."""

    if "source_reliability" in chunk:
        try:
            return float(chunk["source_reliability"])
        except (TypeError, ValueError):
            return 0.5
    trust_tier = str(chunk.get("trust_tier", "public")).lower()
    return {
        "official": 1.0,
        "trusted": 0.8,
        "public": 0.6,
        "unverified": 0.2,
    }.get(trust_tier, 0.5)


def _retrieval_score(chunk: dict[str, Any]) -> float:
    """Return retrieval relevance attached by the search tool."""

    try:
        return float(chunk.get("retrieval_score", 1.0))
    except (TypeError, ValueError):
        return 1.0


def _chunk_tokens(chunk: dict[str, Any]) -> set[str]:
    """Tokenize chunk text and title for novelty estimation."""

    return _text_tokens(str(chunk.get("title", "")) + " " + str(chunk.get("text", "")))


def _text_tokens(value: str) -> set[str]:
    """Tokenize text for deterministic value scoring."""

    stop_words = {"a", "an", "and", "are", "by", "for", "in", "is", "of", "or", "the", "to", "with"}
    return {token for token in re.findall(r"[a-z0-9_]+", value.lower()) if token not in stop_words}


def _round_metric(value: float | int) -> float:
    """Round trace metrics without hiding ordering-relevant precision in code."""

    return round(float(value), 3)


def _has_complete_export_evidence(observed_evidence: list[str]) -> bool:
    """Heuristic gate for high-risk export tools using runtime evidence only."""

    observed = {str(item) for item in observed_evidence}
    return {"user_authorization", "data_scope", "policy_allowance"}.issubset(observed)


def resolve_strategy(name: str) -> AgentStrategy:
    """Resolve a CLI strategy name into a deterministic strategy object."""

    normalized = name.strip().replace("-", "_")
    aliases = {
        "react_agent": "react",
        "plan_execute_agent": "plan_execute",
        "verify_then_answer_agent": "verify_then_answer",
        "context_budget_agent": "context_budget",
        "guarded_agent": "react",
    }
    normalized = aliases.get(normalized, normalized)
    strategies: dict[str, AgentStrategy] = {
        "react": ReactStrategy(),
        "plan_execute": PlanExecuteStrategy(),
        "verify_then_answer": VerifyThenAnswerStrategy(),
        "context_budget": ContextBudgetStrategy(),
        "llm_planner": LLMPlannerStrategy(),
    }
    if normalized not in strategies:
        raise ValueError(f"Unknown strategy: {name}")
    return strategies[normalized]


def parse_strategy_list(value: str) -> list[str]:
    """Parse comma-separated strategy names from the CLI."""

    return [item.strip() for item in value.split(",") if item.strip()]
