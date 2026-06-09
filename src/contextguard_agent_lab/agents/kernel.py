"""Minimal agent kernel.

This file intentionally avoids depending on a hosted LLM. The first
milestone is an auditable control loop; model-backed planning can be
plugged in later.
"""

from __future__ import annotations

from contextguard_agent_lab.agents.state import AgentState
from contextguard_agent_lab.agents.strategies import resolve_strategy
from contextguard_agent_lab.benchmark.schema import CaseSpec, RunRecord
from contextguard_agent_lab.eval.graders import grade_run
from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine
from contextguard_agent_lab.tools.registry import ToolExecutor


class AgentKernel:
    """Small plan-act-observe kernel used by all demo strategies."""

    def __init__(self, tools: ToolExecutor, policy_engine: EvidencePolicyEngine) -> None:
        self.tools = tools
        self.policy_engine = policy_engine

    def run(self, case: CaseSpec, strategy: str = "react") -> RunRecord:
        """Run one case with a deterministic starter policy."""

        strategy_impl = resolve_strategy(strategy)
        state = AgentState(case=case, strategy=strategy_impl.name)
        state.plan = strategy_impl.plan(state)

        if case.case_type == "sensitive_action" and case.sensitive_action:
            decision = self.policy_engine.decide(
                case_id=case.case_id,
                action=case.sensitive_action,
                observed_evidence=case.observed_evidence,
            )
            state.policy_decisions.append(decision)
            answer = f"{decision.decision}: {decision.reason}"
            return self._finalize(
                case,
                RunRecord(
                    case_id=case.case_id,
                    strategy=strategy_impl.name,
                    answer=answer,
                    success=False,
                    family=case.family,
                    budget=case.budget,
                    tool_calls=state.tool_calls,
                    policy_decisions=state.policy_decisions,
                    metrics={"policy_missing_count": len(decision.missing_evidence)},
                ),
            )

        if case.case_type == "rag_qa":
            top_k = strategy_impl.retrieval_top_k(case, state)
            result = self.tools.call("search_docs", {"query": case.user_query, "top_k": top_k})
            state.tool_calls.append(result.trace(case.case_id, step_index=1))
            answer = result.payload.get("answer_hint", "No answer found.")
            if strategy_impl.should_verify_answer(case, state):
                verification = self.tools.call(
                    "verify_citation",
                    {
                        "answer": answer,
                        "doc_ids": result.payload.get("doc_ids", []),
                        "expected_doc_ids": case.expected_outcome.gold_doc_ids,
                    },
                )
                state.tool_calls.append(verification.trace(case.case_id, step_index=2))
            return self._finalize(
                case,
                RunRecord(
                    case_id=case.case_id,
                    strategy=strategy_impl.name,
                    answer=answer,
                    success=False,
                    family=case.family,
                    budget=case.budget,
                    tool_calls=state.tool_calls,
                    policy_decisions=state.policy_decisions,
                    metrics={"tool_call_count": len(state.tool_calls)},
                    cost_proxy=sum(call.cost_proxy for call in state.tool_calls),
                    context_chars_used=sum(call.context_chars for call in state.tool_calls),
                ),
            )

        if case.case_type == "toy_code_repair":
            # The starter skeleton records the intended repair loop
            # without mutating a real workspace yet.
            answer = "stub_not_claimed: repair loop is not implemented in the starter skeleton"
            return self._finalize(
                case,
                RunRecord(
                    case_id=case.case_id,
                    strategy=strategy_impl.name,
                    answer=answer,
                    success=False,
                    family=case.family,
                    budget=case.budget,
                    metrics={"repair_loop_stub": True, "status": "stub_not_claimed"},
                ),
            )

        return self._finalize(
            case,
            RunRecord(
                case_id=case.case_id,
                strategy=strategy_impl.name,
                answer="unsupported case type",
                success=False,
                family=case.family,
                budget=case.budget,
            ),
        )

    def _finalize(self, case: CaseSpec, record: RunRecord) -> RunRecord:
        """Attach independent grader output to a run record."""

        grader_result = grade_run(case, record)
        record.grader_result = grader_result
        record.success = grader_result.success
        record.metrics.update(grader_result.metrics)
        record.metrics["budget_violation"] = grader_result.budget_violation
        return record
