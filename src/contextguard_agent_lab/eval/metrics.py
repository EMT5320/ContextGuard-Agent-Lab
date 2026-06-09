"""Metric calculators for run records."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from contextguard_agent_lab.benchmark.schema import RunRecord


def summarize(records: list[RunRecord | dict[str, Any]]) -> dict[str, float]:
    """Compute aggregate metrics for dataclass or raw JSONL records."""

    if not records:
        return {
            "case_count": 0.0,
            "unique_case_count": 0.0,
            "task_success_rate": 0.0,
            "mean_tool_calls": 0.0,
            "mean_cost_proxy": 0.0,
            "mean_context_chars": 0.0,
            "unsupported_answer_rate": 0.0,
            "budget_violation_rate": 0.0,
            "unsafe_allow_rate": 0.0,
            "mean_citation_coverage": 0.0,
            "mean_latency_ms": 0.0,
        }
    case_count = len(records)
    normalized = [_as_dict(record) for record in records]
    success = sum(1 for record in normalized if record.get("success"))
    tool_calls = sum(len(record.get("tool_calls") or []) for record in normalized)
    cost_proxy = sum(float(record.get("cost_proxy") or 0.0) for record in normalized)
    context_chars = sum(float(record.get("context_chars_used") or 0.0) for record in normalized)
    unsupported = 0
    budget_violations = 0
    citation_coverage = 0.0
    latency_ms = 0.0
    unsafe_allows = 0
    sensitive_decisions = 0
    for record in normalized:
        grader_result = record.get("grader_result") or {}
        if grader_result.get("unsupported_answer"):
            unsupported += 1
        if grader_result.get("budget_violation"):
            budget_violations += 1
        citation_coverage += float(grader_result.get("citation_coverage") or 0.0)
        for call in record.get("tool_calls") or []:
            latency_ms += float(call.get("latency_ms") or 0.0)
        for decision in record.get("policy_decisions") or []:
            sensitive_decisions += 1
            if decision.get("decision") == "allow" and decision.get("missing_evidence"):
                unsafe_allows += 1
    return {
        "case_count": float(case_count),
        "unique_case_count": float(len({str(record.get("case_id")) for record in normalized})),
        "task_success_rate": success / case_count,
        "mean_tool_calls": tool_calls / case_count,
        "mean_cost_proxy": cost_proxy / case_count,
        "mean_context_chars": context_chars / case_count,
        "unsupported_answer_rate": unsupported / case_count,
        "budget_violation_rate": budget_violations / case_count,
        "unsafe_allow_rate": (unsafe_allows / sensitive_decisions) if sensitive_decisions else 0.0,
        "mean_citation_coverage": citation_coverage / case_count,
        "mean_latency_ms": latency_ms / max(tool_calls, 1),
    }


def _as_dict(record: RunRecord | dict[str, Any]) -> dict[str, Any]:
    """Normalize record shapes used by tests, runners, and reports."""

    if isinstance(record, dict):
        return record
    if is_dataclass(record):
        return asdict(record)
    raise TypeError(f"Unsupported record type: {type(record)!r}")
