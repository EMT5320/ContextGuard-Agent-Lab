"""Deterministic agent strategies for the MVP benchmark spine."""

from __future__ import annotations

from typing import Protocol

from contextguard_agent_lab.agents.state import AgentState
from contextguard_agent_lab.benchmark.schema import CaseSpec


class AgentStrategy(Protocol):
    """Strategy interface for deterministic control-policy comparisons."""

    name: str

    def plan(self, state: AgentState) -> list[str]:
        """Return a human-readable strategy plan."""

    def retrieval_top_k(self, case: CaseSpec, state: AgentState) -> int:
        """Choose retrieval depth for a case."""

    def should_verify_answer(self, case: CaseSpec, state: AgentState) -> bool:
        """Decide whether to call a verification tool before final grading."""


class ReactStrategy:
    """Direct observe-act baseline with minimal planning."""

    name = "react"

    def plan(self, state: AgentState) -> list[str]:
        return ["search once", "answer from first observation"]

    def retrieval_top_k(self, case: CaseSpec, state: AgentState) -> int:
        return 1

    def should_verify_answer(self, case: CaseSpec, state: AgentState) -> bool:
        return False


class PlanExecuteStrategy:
    """Plan first, then retrieve enough evidence for multi-hop cases."""

    name = "plan_execute"

    def plan(self, state: AgentState) -> list[str]:
        return ["identify needed evidence", "retrieve multiple candidates", "answer after execution"]

    def retrieval_top_k(self, case: CaseSpec, state: AgentState) -> int:
        return max(2, len(case.expected_outcome.gold_doc_ids))

    def should_verify_answer(self, case: CaseSpec, state: AgentState) -> bool:
        return False


class VerifyThenAnswerStrategy:
    """Always verify support before returning the final answer."""

    name = "verify_then_answer"

    def plan(self, state: AgentState) -> list[str]:
        return ["retrieve evidence", "verify citation support", "answer only after verification"]

    def retrieval_top_k(self, case: CaseSpec, state: AgentState) -> int:
        return max(1, len(case.expected_outcome.gold_doc_ids))

    def should_verify_answer(self, case: CaseSpec, state: AgentState) -> bool:
        return case.budget.max_verification_calls > 0


class ContextBudgetStrategy:
    """Spend as little context and verification budget as possible."""

    name = "context_budget"

    def plan(self, state: AgentState) -> list[str]:
        return ["estimate evidence value", "retrieve within budget", "skip low-value verification"]

    def retrieval_top_k(self, case: CaseSpec, state: AgentState) -> int:
        if case.budget.max_context_chars < 1000 or case.budget.cost_proxy_limit < 4:
            return 1
        return min(2, max(1, len(case.expected_outcome.gold_doc_ids)))

    def should_verify_answer(self, case: CaseSpec, state: AgentState) -> bool:
        return case.budget.cost_proxy_limit >= 6 and case.budget.max_verification_calls > 0


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
