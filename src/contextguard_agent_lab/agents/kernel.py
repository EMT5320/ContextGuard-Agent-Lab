"""Minimal agent kernel.

This file intentionally avoids depending on a hosted LLM. The first
milestone is an auditable control loop; model-backed planning can be
plugged in later.
"""

from __future__ import annotations

from contextguard_agent_lab.agents.state import AgentState
from contextguard_agent_lab.agents.strategies import resolve_strategy
from contextguard_agent_lab.benchmark.schema import CaseSpec, PolicyDecision, RunRecord
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
        state = AgentState(case=case.to_view(), strategy=strategy_impl.name)
        state.plan = strategy_impl.plan(state)

        if case.case_type == "sensitive_action" and case.sensitive_action:
            if not strategy_impl.should_call_sensitive_tool(state.case, state):
                decision = _skipped_sensitive_tool_decision(case)
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
                        plan=list(state.plan),
                        tool_calls=state.tool_calls,
                        policy_decisions=state.policy_decisions,
                        metrics={
                            "policy_missing_count": len(decision.missing_evidence),
                            "sensitive_tool_skipped": True,
                            "tool_call_count": len(state.tool_calls),
                        },
                    ),
                )
            result = self.tools.call(
                case.sensitive_action,
                {
                    "case_id": case.case_id,
                    "action": case.sensitive_action,
                    "observed_evidence": case.observed_evidence,
                },
            )
            state.tool_calls.append(result.trace(case.case_id, step_index=1))
            decision = PolicyDecision(**result.payload["policy_decision"])
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
                    plan=list(state.plan),
                    tool_calls=state.tool_calls,
                    policy_decisions=state.policy_decisions,
                    metrics={"policy_missing_count": len(decision.missing_evidence), "tool_call_count": len(state.tool_calls)},
                    cost_proxy=sum(call.cost_proxy for call in state.tool_calls),
                    context_chars_used=sum(call.context_chars for call in state.tool_calls),
                ),
            )

        if case.case_type == "rag_qa":
            top_k = strategy_impl.retrieval_top_k(state.case, state)
            result = self.tools.call("search_docs", _search_arguments(case, top_k))
            state.tool_calls.append(result.trace(case.case_id, step_index=1))
            chunks = _payload_chunks(result.payload)
            answer_chunks = strategy_impl.select_answer_chunks(chunks, state)
            answer = _compose_answer(answer_chunks)
            answer_source_doc_ids = _chunk_doc_ids(answer_chunks)
            abstained = False
            if strategy_impl.should_verify_answer(state.case, state):
                verification = self.tools.call("verify_citation", _verification_arguments(answer, chunks, answer_source_doc_ids))
                state.tool_calls.append(verification.trace(case.case_id, step_index=2))
                if not verification.payload.get("supported"):
                    if strategy_impl.should_retry_after_verification(state.case, state) and _can_retry_with_verification(case, state):
                        retry = self.tools.call("search_docs", _search_arguments(case, top_k + 1))
                        state.tool_calls.append(retry.trace(case.case_id, step_index=3))
                        chunks = _payload_chunks(retry.payload)
                        answer_chunks = strategy_impl.select_answer_chunks(chunks, state)
                        answer = _compose_answer(answer_chunks)
                        answer_source_doc_ids = _chunk_doc_ids(answer_chunks)
                        retry_verification = self.tools.call(
                            "verify_citation",
                            _verification_arguments(answer, chunks, answer_source_doc_ids),
                        )
                        state.tool_calls.append(retry_verification.trace(case.case_id, step_index=4))
                        abstained = not bool(retry_verification.payload.get("supported"))
                    else:
                        abstained = True
            if abstained:
                answer = "abstain: verification did not support the answer"
                answer_source_doc_ids = []
            return self._finalize(
                case,
                RunRecord(
                    case_id=case.case_id,
                    strategy=strategy_impl.name,
                    answer=answer,
                    success=False,
                    family=case.family,
                    budget=case.budget,
                    plan=list(state.plan),
                    answer_source_doc_ids=answer_source_doc_ids,
                    abstained=abstained,
                    tool_calls=state.tool_calls,
                    policy_decisions=state.policy_decisions,
                    metrics=_run_metrics(state),
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
                    plan=list(state.plan),
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
                plan=list(state.plan),
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


def _payload_chunks(payload: dict) -> list[dict]:
    """Return structured retrieval chunks from a tool payload."""

    return [chunk for chunk in payload.get("chunks", []) if isinstance(chunk, dict)]


def _search_arguments(case: CaseSpec, top_k: int) -> dict:
    """Build retrieval arguments with optional runtime doc-pool scoping."""

    arguments = {"query": case.user_query, "top_k": top_k}
    if case.retrieval_doc_ids:
        arguments["allowed_doc_ids"] = list(case.retrieval_doc_ids)
    return arguments


def _compose_answer(chunks: list[dict]) -> str:
    """Compose a deterministic answer from selected evidence chunks."""

    if not chunks:
        return "No answer found."
    return " ".join(str(chunk.get("text", "")) for chunk in chunks if chunk.get("text")) or "No answer found."


def _chunk_doc_ids(chunks: list[dict]) -> list[str]:
    """Return selected source document ids in trace order."""

    return [str(chunk.get("doc_id")) for chunk in chunks if chunk.get("doc_id")]


def _verification_arguments(answer: str, chunks: list[dict], answer_source_doc_ids: list[str]) -> dict:
    """Build the verifier input without gold labels."""

    return {"answer": answer, "chunks": chunks, "answer_source_doc_ids": answer_source_doc_ids}


def _run_metrics(state: AgentState) -> dict:
    """Build run metrics, including optional strategy-local diagnostics."""

    metrics = {"tool_call_count": len(state.tool_calls)}
    if "selection_reasons" in state.scratchpad:
        metrics["selection_reasons"] = state.scratchpad["selection_reasons"]
    return metrics


def _can_retry_with_verification(case: CaseSpec, state: AgentState) -> bool:
    """Check whether a retry search plus verifier call can fit declared limits."""

    verification_calls = sum(1 for call in state.tool_calls if "verify" in call.tool_name or "support" in call.tool_name)
    return (
        len(state.tool_calls) + 2 <= case.budget.max_tool_calls
        and verification_calls + 1 <= case.budget.max_verification_calls
    )


def _skipped_sensitive_tool_decision(case: CaseSpec) -> PolicyDecision:
    """Record a strategy-level block without invoking the high-risk tool."""

    return PolicyDecision(
        case_id=case.case_id,
        action=case.sensitive_action or "unknown",
        decision="block",
        required_evidence=[],
        observed_evidence=sorted(set(case.observed_evidence)),
        missing_evidence=[],
        reason="strategy skipped high-risk tool call because evidence was incomplete",
    )
