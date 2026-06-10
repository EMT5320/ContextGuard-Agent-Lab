"""Generate representative case cards from benchmark run records."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from contextguard_agent_lab.benchmark.loader import load_cases
from contextguard_agent_lab.benchmark.schema import CaseSpec
from contextguard_agent_lab.trace.jsonl import read_run_records

PREFERRED_DIMENSIONS = ["retrieval_depth", "verification_timing", "budget_pressure", "adversarial_context"]
STRATEGY_ORDER = ["react", "plan_execute", "verify_then_answer", "context_budget"]


def main() -> None:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--run", default="reports/agent_strategy_ablation.jsonl")
    parser.add_argument("--cases", default="data/benchmark/cases.sample.jsonl")
    parser.add_argument("--out", default="reports/case_cards.md")
    parser.add_argument("--max-cards", type=int, default=4)
    args = parser.parse_args()

    records = read_run_records(REPO_ROOT / args.run)
    cases = load_cases(REPO_ROOT / args.cases)
    lines = build_case_cards(records, cases, run_path=args.run, max_cards=args.max_cards)
    target = REPO_ROOT / args.out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote case cards to {args.out}")


def build_case_cards(
    records: list[dict[str, Any]],
    cases: list[CaseSpec],
    run_path: str,
    max_cards: int = 4,
) -> list[str]:
    """Render representative case cards as Markdown lines."""

    selected_cases = select_representative_cases(records, cases, max_cards=max_cards)
    lines = [
        "# Representative Case Cards",
        "",
        "> Seed-suite examples that make current strategy differences inspectable.",
        "",
        "## Overview",
        "",
        f"- Source run trace: `{run_path}`",
        f"- Cards rendered: {len(selected_cases)}",
        "- Selection: split cases first, then high-value dimensions in stable order.",
        "",
    ]
    records_by_case = _group_by(records, "case_id")
    for index, case in enumerate(selected_cases, start=1):
        lines.extend(_case_card(index, case, records_by_case.get(case.case_id, [])))
    return lines


def select_representative_cases(
    records: list[dict[str, Any]],
    cases: list[CaseSpec],
    max_cards: int = 4,
) -> list[CaseSpec]:
    """Select split cases with deterministic dimension coverage."""

    case_by_id = {case.case_id: case for case in cases}
    records_by_case = _group_by(records, "case_id")
    split_case_ids = {
        case_id
        for case_id, rows in records_by_case.items()
        if case_id in case_by_id and _has_success_split(rows)
    }
    selected: list[CaseSpec] = []
    selected_ids: set[str] = set()

    for dimension in PREFERRED_DIMENSIONS:
        candidates = [
            case_by_id[case_id]
            for case_id in sorted(split_case_ids)
            if case_id not in selected_ids and dimension in case_by_id[case_id].dimensions
        ]
        if candidates:
            selected.append(candidates[0])
            selected_ids.add(candidates[0].case_id)
        if len(selected) >= max_cards:
            return selected

    for case_id in sorted(split_case_ids):
        if case_id not in selected_ids:
            selected.append(case_by_id[case_id])
            selected_ids.add(case_id)
        if len(selected) >= max_cards:
            return selected

    for case in sorted(cases, key=lambda item: item.case_id):
        if case.case_id not in selected_ids:
            selected.append(case)
            selected_ids.add(case.case_id)
        if len(selected) >= max_cards:
            return selected

    return selected


def _case_card(index: int, case: CaseSpec, rows: list[dict[str, Any]]) -> list[str]:
    """Render one case card."""

    winners = [str(row.get("strategy")) for row in _sorted_rows(rows) if row.get("success")]
    losers = [str(row.get("strategy")) for row in _sorted_rows(rows) if not row.get("success")]
    intended_split = str(case.metadata.get("intended_split", "No intended split recorded."))
    lines = [
        f"## Card {index}: `{case.case_id}`",
        "",
        f"- Family: `{case.family}`",
        f"- Dimensions: `{', '.join(case.dimensions) or 'none'}`",
        f"- Intended split: {intended_split}",
        f"- Query: {_escape(case.user_query)}",
        f"- Winners: {_escape(', '.join(winners) or 'none')}",
        f"- Losers: {_escape(', '.join(losers) or 'none')}",
        "",
        "| strategy | success | sources | abstained | tools | cost | context | unsupported | missing_verification | budget_violation | grader_reason |",
        "|---|---:|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in _sorted_rows(rows):
        grader_result = row.get("grader_result") or {}
        grader_metrics = grader_result.get("metrics") or {}
        sources = ", ".join(str(doc_id) for doc_id in row.get("answer_source_doc_ids") or []) or "-"
        lines.append(
            "| "
            f"{_escape(row.get('strategy'))} | "
            f"{row.get('success')} | "
            f"{_escape(sources)} | "
            f"{row.get('abstained', False)} | "
            f"{_escape(_tool_sequence(row))} | "
            f"{float(row.get('cost_proxy') or 0.0):.3f} | "
            f"{int(row.get('context_chars_used') or 0)} | "
            f"{grader_result.get('unsupported_answer', False)} | "
            f"{grader_metrics.get('missing_verification', False)} | "
            f"{grader_result.get('budget_violation', False)} | "
            f"{_escape(grader_result.get('reason', ''))} |"
        )
    lines.extend([
        "",
        "**What this demonstrates:** " + _interpretation(case, winners, losers),
        "",
    ])
    return lines


def _interpretation(case: CaseSpec, winners: list[str], losers: list[str]) -> str:
    """Explain the strategy signal for a card."""

    dimensions = set(case.dimensions)
    if "verification_timing" in dimensions:
        return "Verification timing is visible because strategies that call support checks can separate from direct-answer baselines."
    if "budget_pressure" in dimensions:
        return "Budget pressure is visible because strategies differ on context and cost constraints under the same case budget."
    if "adversarial_context" in dimensions:
        return "Adversarial context behavior is visible because strategies face poisoned or distracting evidence under one shared grader."
    if "retrieval_depth" in dimensions:
        return "Retrieval depth is visible because shallow search can miss required documents while deeper plans recover them."
    if winners and losers:
        return "The shared case produces a measurable strategy split under independent grading."
    return "The card is included for inspection even though this seed run produced no strategy split."


def _has_success_split(rows: list[dict[str, Any]]) -> bool:
    """Return true when strategies disagree on success."""

    outcomes = {bool(row.get("success")) for row in rows}
    return len(outcomes) > 1


def _sorted_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort rows by MVP strategy order and then name."""

    return sorted(rows, key=lambda row: (_strategy_index(str(row.get("strategy", ""))), str(row.get("strategy", ""))))


def _strategy_index(strategy: str) -> int:
    """Return stable strategy ordering for report tables."""

    try:
        return STRATEGY_ORDER.index(strategy)
    except ValueError:
        return len(STRATEGY_ORDER)


def _tool_sequence(record: dict[str, Any]) -> str:
    """Format a compact tool sequence."""

    calls = record.get("tool_calls") or []
    return " -> ".join(str(call.get("tool_name", "")) for call in calls) or "-"


def _group_by(records: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    """Group records by a stable string key."""

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[str(record.get(key) or "unknown")].append(record)
    return groups


def _escape(value: Any) -> str:
    """Escape Markdown table cell content."""

    return str(value if value is not None else "").replace("|", "/").replace("\n", " ")


if __name__ == "__main__":
    main()
