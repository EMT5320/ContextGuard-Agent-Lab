"""Generate a context-budget success-cost frontier report."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from contextguard_agent_lab.eval.metrics import summarize
from contextguard_agent_lab.trace.jsonl import read_run_records


def main() -> None:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--run", default="reports/agent_strategy_ablation.jsonl")
    parser.add_argument("--out", default="reports/context_budget_frontier.md")
    args = parser.parse_args()

    records = read_run_records(REPO_ROOT / args.run)
    lines = build_frontier_report(records, run_path=args.run)
    target = REPO_ROOT / args.out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote frontier report to {args.out}")


def build_frontier_report(records: list[dict[str, Any]], run_path: str) -> list[str]:
    """Render the success-cost frontier report as Markdown lines."""

    core_records = _core_records(records)
    overall = summarize(core_records)
    points = strategy_points(core_records)
    dominated = dominated_strategies(points)
    lines = [
        "# Context Budget Frontier",
        "",
        "> Seed-suite success-cost view for deterministic MVP strategies.",
        "",
        "## Overview",
        "",
        f"- Source run trace: `{run_path}`",
        f"- Run records: {len(records)}",
        f"- Core aggregate records: {int(overall['case_count'])}",
        f"- Excluded coding fixture records: {len(records) - len(core_records)}",
        f"- Unique cases: {int(overall['unique_case_count'])}",
        f"- Strategies: {len(points)}",
        f"- Overall success rate: {_pct(overall['task_success_rate'])}",
        "",
        "## Success-Cost Table",
        "",
        "| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for point in sorted(points, key=lambda item: (item["mean_cost"], item["strategy"])):
        note = "dominated in this seed run" if point["strategy"] in dominated else "on current seed frontier"
        lines.append(
            "| "
            f"{_escape(point['strategy'])} | "
            f"{_pct(point['success_rate'])} | "
            f"{point['mean_cost']:.3f} | "
            f"{point['mean_context']:.1f} | "
            f"{_pct(point['budget_rate'])} | "
            f"{note} |"
        )
    lines.extend([
        "",
        "## Pareto Notes",
        "",
    ])
    if dominated:
        lines.append("- Dominated strategies in this seed run: " + ", ".join(sorted(dominated)) + ".")
    else:
        lines.append("- No dominated strategy was observed in this seed run.")
    lines.append("- Dominance uses success rate and mean cost only; context and budget violations remain visible diagnostics.")
    lines.extend([
        "",
        "## Context Budget Focus",
        "",
    ])
    lines.extend(_context_budget_focus(core_records))
    lines.extend([
        "",
        "## Selection Trace Samples",
        "",
    ])
    lines.extend(_selection_trace_samples(core_records))
    lines.extend([
        "",
        "## Value Heuristic",
        "",
        "The current `context_budget` skeleton records a label-free greedy value signal:",
        "",
        "```text",
        "chunk_value = query_relevance * source_reliability * novelty",
        "chunk_cost = estimated_context_chars",
        "selection_score = chunk_value / max(chunk_cost, 1)",
        "```",
        "",
        "Selection reasons are emitted under `record.metrics.selection_reasons`; the next upgrade is to tune this heuristic against larger case coverage.",
        "",
    ])
    return lines


def strategy_points(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate strategy-level success-cost points."""

    points: list[dict[str, Any]] = []
    for strategy, rows in _group_by(records, "strategy").items():
        metrics = summarize(rows)
        points.append(
            {
                "strategy": strategy,
                "success_rate": metrics["task_success_rate"],
                "mean_cost": metrics["mean_cost_proxy"],
                "mean_context": metrics["mean_context_chars"],
                "budget_rate": metrics["budget_violation_rate"],
            }
        )
    return points


def dominated_strategies(points: list[dict[str, Any]]) -> set[str]:
    """Find strategies dominated by another strategy on success and mean cost."""

    dominated: set[str] = set()
    for candidate in points:
        for challenger in points:
            if candidate["strategy"] == challenger["strategy"]:
                continue
            no_worse = (
                challenger["success_rate"] >= candidate["success_rate"]
                and challenger["mean_cost"] <= candidate["mean_cost"]
            )
            strictly_better = (
                challenger["success_rate"] > candidate["success_rate"]
                or challenger["mean_cost"] < candidate["mean_cost"]
            )
            if no_worse and strictly_better:
                dominated.add(candidate["strategy"])
                break
    return dominated


def _context_budget_focus(records: list[dict[str, Any]]) -> list[str]:
    """Summarize context_budget split wins and losses."""

    rows_by_case = _group_by(records, "case_id")
    wins: list[str] = []
    losses: list[str] = []
    neutral: list[str] = []
    for case_id, rows in sorted(rows_by_case.items()):
        context_row = next((row for row in rows if row.get("strategy") == "context_budget"), None)
        if context_row is None:
            continue
        other_rows = [row for row in rows if row.get("strategy") != "context_budget"]
        other_success = any(bool(row.get("success")) for row in other_rows)
        other_failure = any(not bool(row.get("success")) for row in other_rows)
        if context_row.get("success") and other_failure:
            wins.append(case_id)
        elif not context_row.get("success") and other_success:
            losses.append(case_id)
        else:
            neutral.append(case_id)

    lines = [
        f"- Split wins for `context_budget`: {_format_case_list(wins)}",
        f"- Split losses for `context_budget`: {_format_case_list(losses)}",
        f"- Same-outcome cases for `context_budget`: {_format_case_list(neutral)}",
    ]
    if wins:
        lines.append("- Current value: the budget strategy can preserve success where another strategy fails under cost or evidence constraints.")
    if losses:
        lines.append("- Current limitation: the budget strategy can still miss evidence when its conservative retrieval choice is too shallow.")
    if not wins and not losses:
        lines.append("- Current observation: this run did not isolate a context_budget-only split.")
    return lines


def _selection_trace_samples(records: list[dict[str, Any]], limit: int = 5) -> list[str]:
    """Render compact context-budget chunk selection diagnostics."""

    rows = [
        record
        for record in records
        if record.get("strategy") == "context_budget" and (record.get("metrics") or {}).get("selection_reasons")
    ]
    if not rows:
        return ["- No context-budget selection reasons were emitted in this run."]

    lines: list[str] = []
    for row in sorted(rows, key=lambda item: (not _has_skipped_selection(item), str(item.get("case_id", ""))))[:limit]:
        reasons = (row.get("metrics") or {}).get("selection_reasons") or []
        selected = [str(reason.get("doc_id")) for reason in reasons if reason.get("selected")]
        skipped = [
            f"`{_escape(reason.get('doc_id'))}` ({_escape(reason.get('skipped_reason'))})"
            for reason in reasons
            if not reason.get("selected")
        ]
        lines.append(
            f"- `{_escape(row.get('case_id'))}` selected {_format_doc_list(selected)}; skipped {_format_inline_list(skipped)}."
        )
    return lines


def _has_skipped_selection(record: dict[str, Any]) -> bool:
    """Return true when a context-budget row skipped at least one chunk."""

    reasons = (record.get("metrics") or {}).get("selection_reasons") or []
    return any(not reason.get("selected") for reason in reasons)


def _format_case_list(case_ids: list[str]) -> str:
    """Format case ids for a Markdown bullet."""

    if not case_ids:
        return "none"
    return ", ".join(f"`{case_id}`" for case_id in case_ids)


def _format_doc_list(doc_ids: list[str]) -> str:
    """Format document ids for inline Markdown."""

    if not doc_ids:
        return "none"
    return ", ".join(f"`{_escape(doc_id)}`" for doc_id in doc_ids)


def _format_inline_list(items: list[str]) -> str:
    """Format pre-rendered inline Markdown fragments."""

    if not items:
        return "none"
    return ", ".join(items)


def _group_by(records: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    """Group raw records by a stable string key."""

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[str(record.get(key) or "unknown")].append(record)
    return groups


def _core_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Exclude unimplemented coding fixtures from frontier aggregates."""

    return [record for record in records if record.get("family") != "coding_fixture"]


def _pct(value: float) -> str:
    """Format a ratio as a compact percentage."""

    return f"{value * 100:.1f}%"


def _escape(value: Any) -> str:
    """Escape Markdown table cell content."""

    return str(value if value is not None else "").replace("|", "/").replace("\n", " ")


if __name__ == "__main__":
    main()
