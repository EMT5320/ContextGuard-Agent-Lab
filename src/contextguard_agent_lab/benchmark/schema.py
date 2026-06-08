"""Typed benchmark records for ContextGuard Agent Lab.

The project keeps schemas small and explicit so reports can be audited
without loading a large framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

CaseType = Literal["rag_qa", "prompt_injection", "retrieval_poisoning", "sensitive_action", "toy_code_repair"]
Decision = Literal["allow", "block", "review"]


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
    metadata: dict[str, Any] = field(default_factory=dict)


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
    tool_calls: list[ToolCallTrace] = field(default_factory=list)
    policy_decisions: list[PolicyDecision] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
