"""Deterministic agent strategies for the MVP benchmark spine."""

from __future__ import annotations

from typing import Any, Protocol

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


class ContextBudgetStrategy:
    """Spend as little context and verification budget as possible."""

    name = "context_budget"

    def plan(self, state: AgentState) -> list[str]:
        return ["estimate evidence value", "retrieve within budget", "skip low-value verification"]

    def retrieval_top_k(self, case: CaseView, state: AgentState) -> int:
        if case.budget.max_context_chars < 1600 or case.budget.cost_proxy_limit < 6:
            return 1
        return 2

    def select_answer_chunks(self, chunks: list[dict[str, Any]], state: AgentState) -> list[dict[str, Any]]:
        return _select_most_reliable_chunks(chunks)

    def should_verify_answer(self, case: CaseView, state: AgentState) -> bool:
        return case.budget.cost_proxy_limit >= 6 and case.budget.max_verification_calls > 0

    def should_retry_after_verification(self, case: CaseView, state: AgentState) -> bool:
        return False


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
    }
    if normalized not in strategies:
        raise ValueError(f"Unknown strategy: {name}")
    return strategies[normalized]


def parse_strategy_list(value: str) -> list[str]:
    """Parse comma-separated strategy names from the CLI."""

    return [item.strip() for item in value.split(",") if item.strip()]
