"""Minimal agent kernel.

This file intentionally avoids depending on a hosted LLM. The first
milestone is an auditable control loop; model-backed planning can be
plugged in later.
"""

from __future__ import annotations

from contextguard_agent_lab.agents.state import AgentState
from contextguard_agent_lab.benchmark.schema import CaseSpec, RunRecord
from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine
from contextguard_agent_lab.tools.registry import ToolRegistry


class AgentKernel:
    """Small plan-act-observe kernel used by all demo strategies."""

    def __init__(self, tools: ToolRegistry, policy_engine: EvidencePolicyEngine) -> None:
        self.tools = tools
        self.policy_engine = policy_engine

    def run(self, case: CaseSpec, strategy: str = "guarded_agent") -> RunRecord:
        """Run one case with a deterministic starter policy."""

        state = AgentState(case=case, strategy=strategy)
        state.plan = self._plan(case, strategy)

        if case.case_type == "sensitive_action" and case.sensitive_action:
            decision = self.policy_engine.decide(
                case_id=case.case_id,
                action=case.sensitive_action,
                observed_evidence=case.observed_evidence,
            )
            state.policy_decisions.append(decision)
            answer = f"{decision.decision}: {decision.reason}"
            success = decision.decision == "block" and bool(decision.missing_evidence)
            return RunRecord(
                case_id=case.case_id,
                strategy=strategy,
                answer=answer,
                success=success,
                tool_calls=state.tool_calls,
                policy_decisions=state.policy_decisions,
                metrics={"policy_missing_count": len(decision.missing_evidence)},
            )

        if case.case_type == "rag_qa":
            result = self.tools.call("search_docs", {"query": case.user_query, "top_k": 1})
            state.tool_calls.append(result.trace(case.case_id, step_index=1))
            answer = result.payload.get("answer_hint", "No answer found.")
            success = all(doc_id in result.payload.get("doc_ids", []) for doc_id in case.gold_doc_ids)
            return RunRecord(
                case_id=case.case_id,
                strategy=strategy,
                answer=answer,
                success=success,
                tool_calls=state.tool_calls,
                policy_decisions=state.policy_decisions,
                metrics={"tool_call_count": len(state.tool_calls)},
            )

        if case.case_type == "toy_code_repair":
            # The starter skeleton records the intended repair loop
            # without mutating a real workspace yet.
            answer = "stub_not_claimed: repair loop is not implemented in the starter skeleton"
            return RunRecord(
                case_id=case.case_id,
                strategy=strategy,
                answer=answer,
                success=False,
                metrics={"repair_loop_stub": True, "status": "stub_not_claimed"},
            )

        return RunRecord(case_id=case.case_id, strategy=strategy, answer="unsupported case type", success=False)

    def _plan(self, case: CaseSpec, strategy: str) -> list[str]:
        """Create a simple plan for trace readability."""

        if case.case_type == "rag_qa":
            return ["search relevant docs", "verify gold citation", "answer with source"]
        if case.case_type == "sensitive_action":
            return ["collect evidence", "evaluate policy", "allow/block/review"]
        if case.case_type == "toy_code_repair":
            return ["read failing test", "apply patch", "rerun tests"]
        return [f"handle with {strategy}"]
