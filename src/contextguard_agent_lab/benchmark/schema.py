"""Typed benchmark records for ContextGuard Agent Lab.

The project keeps schemas small and explicit so reports can be audited
without loading a large framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

CaseType = Literal["rag_qa", "prompt_injection", "retrieval_poisoning", "sensitive_action", "toy_code_repair"]
CaseFamily = Literal[
    "retrieval_qa",
    "adversarial_context",
    "verification_needed",
    "budget_pressure",
    "tool_selection",
    "sensitive_action",
    "coding_fixture",
]
StrategyDimension = Literal[
    "retrieval_depth",
    "verification_timing",
    "budget_pressure",
    "adversarial_context",
    "tool_boundary",
]
Decision = Literal["allow", "block", "review"]


@dataclass(slots=True)
class BudgetSpec:
    """Per-case budget limits used by cost-aware strategies and graders."""

    max_tool_calls: int = 8
    max_context_chars: int = 4000
    max_verification_calls: int = 2
    cost_proxy_limit: float = 12.0


@dataclass(slots=True)
class ExpectedOutcome:
    """Expected result fields independent graders can check."""

    answer: str = ""
    gold_doc_ids: list[str] = field(default_factory=list)
    required_evidence: list[str] = field(default_factory=list)
    sensitive_decision: Decision | None = None
    status: str | None = None


@dataclass(slots=True)
class GraderSpec:
    """Selects how a case should be graded."""

    grader_type: str = "auto"
    require_citation: bool = False
    allow_partial: bool = False


@dataclass(slots=True)
class GraderResult:
    """Independent grading output for one run."""

    success: bool
    grader_type: str
    unsupported_answer: bool = False
    citation_coverage: float = 0.0
    budget_violation: bool = False
    reason: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CaseSpec:
    """One benchmark case shared by all agent strategies."""

    case_id: str
    case_type: CaseType
    user_query: str
    expected_answer: str
    gold_doc_ids: list[str] = field(default_factory=list)
    required_evidence: list[str] = field(default_factory=list)
    observed_evidence: list[str] = field(default_factory=list)
    sensitive_action: str | None = None
    workspace_task: dict[str, Any] | None = None
    family: CaseFamily | None = None
    dimensions: list[StrategyDimension] = field(default_factory=list)
    budget: BudgetSpec | dict[str, Any] = field(default_factory=BudgetSpec)
    expected_outcome: ExpectedOutcome | dict[str, Any] | None = None
    grader: GraderSpec | dict[str, Any] = field(default_factory=GraderSpec)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Normalize nested schema values loaded from JSON."""

        if isinstance(self.budget, dict):
            self.budget = BudgetSpec(**self.budget)
        if isinstance(self.grader, dict):
            self.grader = GraderSpec(**self.grader)
        if isinstance(self.expected_outcome, dict):
            self.expected_outcome = ExpectedOutcome(**self.expected_outcome)
        if self.expected_outcome is None:
            self.expected_outcome = ExpectedOutcome(
                answer=self.expected_answer,
                gold_doc_ids=list(self.gold_doc_ids),
                required_evidence=list(self.required_evidence),
                sensitive_decision=self._default_sensitive_decision(),
            )
        if self.family is None:
            self.family = self._default_family()

    def _default_family(self) -> CaseFamily:
        """Map legacy case types into the newer case-family vocabulary."""

        if self.case_type in {"prompt_injection", "retrieval_poisoning"}:
            return "adversarial_context"
        if self.case_type == "sensitive_action":
            return "sensitive_action"
        if self.case_type == "toy_code_repair":
            return "coding_fixture"
        return "retrieval_qa"

    def _default_sensitive_decision(self) -> Decision | None:
        """Derive the expected sensitive decision for legacy sample cases."""

        if self.case_type != "sensitive_action":
            return None
        return "block" if self.required_evidence else None


@dataclass(slots=True)
class ToolCallTrace:
    """Trace for a single tool call.

    Keeping every call structured makes later unsafe-allow and
    wrong-tool analysis possible.
    """

    case_id: str
    step_index: int
    tool_name: str
    arguments: dict[str, Any]
    result: dict[str, Any]
    latency_ms: int = 0
    cost_proxy: float = 0.0
    context_chars: int = 0
    risk_level: str = "low"


@dataclass(slots=True)
class PolicyDecision:
    """Evidence-gated decision for a sensitive action."""

    case_id: str
    action: str
    decision: Decision
    required_evidence: list[str]
    observed_evidence: list[str]
    missing_evidence: list[str]
    reason: str


@dataclass(slots=True)
class RunRecord:
    """Final result for one case and one strategy."""

    case_id: str
    strategy: str
    answer: str
    success: bool
    family: str | None = None
    budget: BudgetSpec | None = None
    grader_result: GraderResult | None = None
    tool_calls: list[ToolCallTrace] = field(default_factory=list)
    policy_decisions: list[PolicyDecision] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    cost_proxy: float = 0.0
    context_chars_used: int = 0
