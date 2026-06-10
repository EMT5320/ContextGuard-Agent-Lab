"""Generate Markdown reports from JSONL benchmark runs."""

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
    parser.add_argument("--run", default="reports/sample_run.jsonl")
    parser.add_argument("--out", default="reports/sample_report.md")
    args = parser.parse_args()

    records = read_run_records(REPO_ROOT / args.run)
    target = REPO_ROOT / args.out
    lines = build_report(records, run_path=args.run, out_path=args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote report to {args.out}")


def build_report(records: list[dict[str, Any]], run_path: str, out_path: str) -> list[str]:
    """Build a Markdown ablation report from raw run records."""

    title = "Starter Smoke Report" if "sample" in Path(out_path).name else "Agent Strategy Ablation Report"
    subtitle = _subtitle(title)
    overall = summarize(records)
    lines = [
        f"# {title}",
        "",
        subtitle,
        "",
        "## Overview",
        "",
        f"- Run trace: `{run_path}`",
        f"- Run records: {int(overall['case_count'])}",
        f"- Unique cases: {int(overall['unique_case_count'])}",
        f"- Overall success rate: {_pct(overall['task_success_rate'])}",
        f"- Unsupported answer rate: {_pct(overall['unsupported_answer_rate'])}",
        f"- Budget violation rate: {_pct(overall['budget_violation_rate'])}",
        "",
    ]
    lines.extend(_summary_section("By Strategy", _group_by(records, "strategy")))
    lines.extend(_summary_section("By Family", _group_by(records, "family")))
    lines.extend(_frontier_section(records))
    lines.extend(_split_section(records))
    lines.extend(_detail_section(records))
    lines.extend(_failure_section(records))
    return lines


def _subtitle(title: str) -> str:
    """Return honest report positioning for the selected artifact."""

    if title == "Starter Smoke Report":
        return "> Starter artifact with aggregate metrics. It checks wiring and early strategy separation."
    return "> MVP-oriented report across shared cases, deterministic strategies, tool traces, and independent grader output."


def _summary_section(title: str, groups: dict[str, list[dict[str, Any]]]) -> list[str]:
    """Render aggregate metrics for a group map."""

    lines = [
        f"## {title}",
        "",
        "| group | runs | success_rate | unsupported_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for group_name in sorted(groups):
        metrics = summarize(groups[group_name])
        lines.append(
            "| "
            f"{_escape(group_name)} | "
            f"{int(metrics['case_count'])} | "
            f"{_pct(metrics['task_success_rate'])} | "
            f"{_pct(metrics['unsupported_answer_rate'])} | "
            f"{_pct(metrics['budget_violation_rate'])} | "
            f"{metrics['mean_tool_calls']:.2f} | "
            f"{metrics['mean_cost_proxy']:.3f} | "
            f"{metrics['mean_context_chars']:.1f} |"
        )
    lines.append("")
    return lines


def _frontier_section(records: list[dict[str, Any]]) -> list[str]:
    """Render a small success-cost frontier table."""

    by_strategy = _group_by(records, "strategy")
    points: list[dict[str, Any]] = []
    for strategy, rows in by_strategy.items():
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
    dominated = _dominated_strategies(points)
    lines = [
        "## Success-Cost View",
        "",
        "| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for point in sorted(points, key=lambda item: (item["mean_cost"], item["strategy"])):
        note = "dominated in this run" if point["strategy"] in dominated else "on current frontier"
        lines.append(
            "| "
            f"{_escape(point['strategy'])} | "
            f"{_pct(point['success_rate'])} | "
            f"{point['mean_cost']:.3f} | "
            f"{point['mean_context']:.1f} | "
            f"{_pct(point['budget_rate'])} | "
            f"{note} |"
        )
    lines.append("")
    return lines


def _dominated_strategies(points: list[dict[str, Any]]) -> set[str]:
    """Find strategies with no better success-cost tradeoff than another strategy."""

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


def _split_section(records: list[dict[str, Any]]) -> list[str]:
    """List cases where strategies produced different success outcomes."""

    by_case = _group_by(records, "case_id")
    split_cases = []
    for case_id, rows in sorted(by_case.items()):
        outcomes = {bool(row.get("success")) for row in rows}
        if len(outcomes) <= 1:
            continue
        winners = [row.get("strategy", "") for row in rows if row.get("success")]
        losers = [row.get("strategy", "") for row in rows if not row.get("success")]
        split_cases.append((case_id, rows[0].get("family", ""), winners, losers))
    lines = [
        "## Observed Strategy Splits",
        "",
        "| case_id | family | successful_strategies | failed_strategies |",
        "|---|---|---|---|",
    ]
    if not split_cases:
        lines.append("| _none_ |  |  |  |")
    for case_id, family, winners, losers in split_cases:
        lines.append(
            "| "
            f"{_escape(case_id)} | "
            f"{_escape(str(family))} | "
            f"{_escape(', '.join(winners))} | "
            f"{_escape(', '.join(losers))} |"
        )
    lines.append("")
    return lines


def _detail_section(records: list[dict[str, Any]]) -> list[str]:
    """Render compact per-run trace rows."""

    lines = [
        "## Run Detail",
        "",
        "| case_id | family | strategy | success | sources | abstained | tools | cost | context | unsupported | budget_violation | grader_reason |",
        "|---|---|---|---:|---|---:|---|---:|---:|---:|---:|---|",
    ]
    for record in sorted(records, key=lambda item: (item.get("case_id", ""), item.get("strategy", ""))):
        grader_result = record.get("grader_result") or {}
        tool_sequence = " -> ".join(call.get("tool_name", "") for call in record.get("tool_calls") or []) or "-"
        sources = ", ".join(str(doc_id) for doc_id in record.get("answer_source_doc_ids") or []) or "-"
        lines.append(
            "| "
            f"{_escape(record.get('case_id'))} | "
            f"{_escape(record.get('family'))} | "
            f"{_escape(record.get('strategy'))} | "
            f"{record.get('success')} | "
            f"{_escape(sources)} | "
            f"{record.get('abstained', False)} | "
            f"{_escape(tool_sequence)} | "
            f"{float(record.get('cost_proxy') or 0.0):.3f} | "
            f"{int(record.get('context_chars_used') or 0)} | "
            f"{grader_result.get('unsupported_answer', False)} | "
            f"{grader_result.get('budget_violation', False)} | "
            f"{_escape(grader_result.get('reason', ''))} |"
        )
    lines.append("")
    return lines


def _failure_section(records: list[dict[str, Any]]) -> list[str]:
    """Render a bounded list of failure examples for reviewer inspection."""

    failures = [record for record in records if not record.get("success")]
    lines = [
        "## Failure Highlights",
        "",
        "| case_id | strategy | failure_mode | reason |",
        "|---|---|---|---|",
    ]
    if not failures:
        lines.append("| _none_ |  |  |  |")
    for record in failures[:12]:
        grader_result = record.get("grader_result") or {}
        failure_mode = _failure_mode(grader_result)
        lines.append(
            "| "
            f"{_escape(record.get('case_id'))} | "
            f"{_escape(record.get('strategy'))} | "
            f"{failure_mode} | "
            f"{_escape(grader_result.get('reason', ''))} |"
        )
    lines.append("")
    return lines


def _failure_mode(grader_result: dict[str, Any]) -> str:
    """Classify a failure from grader flags."""

    if grader_result.get("metrics", {}).get("abstained"):
        return "abstained"
    if grader_result.get("budget_violation"):
        return "budget_violation"
    if grader_result.get("unsupported_answer"):
        return "unsupported_answer"
    return "grader_failure"


def _group_by(records: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    """Group raw records by a stable string key."""

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[str(record.get(key) or "unknown")].append(record)
    return groups


def _pct(value: float) -> str:
    """Format a ratio as a compact percentage."""

    return f"{value * 100:.1f}%"


def _escape(value: Any) -> str:
    """Escape Markdown table cell content."""

    return str(value if value is not None else "").replace("|", "/").replace("\n", " ")


if __name__ == "__main__":
    main()
