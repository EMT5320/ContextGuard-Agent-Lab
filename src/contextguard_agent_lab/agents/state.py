"""Mutable state used by the agent loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from contextguard_agent_lab.benchmark.schema import CaseView, PolicyDecision, ToolCallTrace


@dataclass(slots=True)
class AgentState:
    """State passed between plan, tool execution, and reflection steps."""

    case: CaseView
    strategy: str
    plan: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    tool_calls: list[ToolCallTrace] = field(default_factory=list)
    policy_decisions: list[PolicyDecision] = field(default_factory=list)
    scratchpad: dict[str, Any] = field(default_factory=dict)
