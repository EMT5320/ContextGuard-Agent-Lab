# Showcase Entry Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build reproducible Markdown showcase artifacts that explain representative strategy splits, context-budget tradeoffs, and claim-to-evidence links for ContextGuard Agent Lab.

**Architecture:** Add two focused generator scripts under `scripts/` that consume existing JSONL run records and case specs, then render deterministic Markdown reports under `reports/`. Keep the display layer artifact-driven by updating `README.md` and `reports/README.md` with concrete links and regeneration commands.

**Tech Stack:** Python 3.10+, standard library, existing `contextguard_agent_lab` loaders, existing `summarize()` metric helper, `unittest`, Markdown.

---

## Scope Check

The approved spec covers one cohesive showcase upgrade. It creates generated report artifacts, report-index links, README evidence links, and small deterministic tests. It does not require a separate sub-project split.

## File Structure

- Create: `scripts/generate_case_cards.py`
  - Responsibility: load ablation run records and case specs, select representative split cases, render `reports/case_cards.md`.
- Create: `scripts/generate_frontier_report.py`
  - Responsibility: load ablation run records, compute success-cost points, classify dominated strategies, render `reports/context_budget_frontier.md`.
- Create: `tests/test_case_cards_report.py`
  - Responsibility: verify case-card selection and Markdown rendering.
- Create: `tests/test_frontier_report.py`
  - Responsibility: verify dominance classification and frontier Markdown rendering.
- Create: `tests/test_showcase_docs.py`
  - Responsibility: verify README and report index contain the showcase links and regeneration commands.
- Modify: `README.md`
  - Responsibility: add a concise claim-evidence table linked to concrete artifacts.
- Modify: `reports/README.md`
  - Responsibility: index the new generated artifacts and document regeneration commands.
- Generate: `reports/case_cards.md`
  - Responsibility: reviewer-facing case split explanations.
- Generate: `reports/context_budget_frontier.md`
  - Responsibility: reviewer-facing success-cost and context-budget analysis.

---

### Task 1: Add failing tests for case-card selection and rendering

**Files:**
- Create: `tests/test_case_cards_report.py`
- Later implementation target: `scripts/generate_case_cards.py`

- [ ] **Step 1: Write the failing case-card tests**

Create `tests/test_case_cards_report.py` with this exact content:

```python
"""Tests for generated strategy case cards."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contextguard_agent_lab.benchmark.schema import CaseSpec
from scripts.generate_case_cards import build_case_cards, select_representative_cases


class CaseCardsReportTest(unittest.TestCase):
    """Case-card generator unit tests."""

    def test_selection_prefers_split_cases_by_dimension_order(self) -> None:
        """Representative cards should prioritize high-value split dimensions."""

        cases = [
            CaseSpec(
                case_id="cg_rag_split",
                case_type="rag_qa",
                family="retrieval_qa",
                dimensions=["retrieval_depth"],
                user_query="Need two docs",
                expected_answer="answer",
                gold_doc_ids=["doc-a", "doc-b"],
                metadata={"intended_split": "plan_execute should beat react"},
            ),
            CaseSpec(
                case_id="cg_verify_split",
                case_type="rag_qa",
                family="verification_needed",
                dimensions=["verification_timing"],
                user_query="Need verification",
                expected_answer="answer",
                gold_doc_ids=["doc-v"],
                metadata={"intended_split": "verify_then_answer should win"},
            ),
            CaseSpec(
                case_id="cg_budget_split",
                case_type="rag_qa",
                family="budget_pressure",
                dimensions=["budget_pressure"],
                user_query="Need compact evidence",
                expected_answer="answer",
                gold_doc_ids=["doc-b"],
                metadata={"intended_split": "context_budget should avoid over-retrieval"},
            ),
        ]
        records = [
            _record("cg_rag_split", "react", False, "retrieval_qa"),
            _record("cg_rag_split", "plan_execute", True, "retrieval_qa"),
            _record("cg_verify_split", "react", False, "verification_needed"),
            _record("cg_verify_split", "verify_then_answer", True, "verification_needed"),
            _record("cg_budget_split", "plan_execute", False, "budget_pressure", budget=True),
            _record("cg_budget_split", "context_budget", True, "budget_pressure"),
        ]

        selected = select_representative_cases(records, cases, max_cards=3)

        self.assertEqual([case.case_id for case in selected], ["cg_rag_split", "cg_verify_split", "cg_budget_split"])

    def test_build_case_cards_renders_required_sections(self) -> None:
        """Markdown output should include card metadata, strategy rows, and interpretation."""

        case = CaseSpec(
            case_id="cg_rag_split",
            case_type="rag_qa",
            family="retrieval_qa",
            dimensions=["retrieval_depth"],
            user_query="Need two docs",
            expected_answer="answer",
            gold_doc_ids=["doc-a", "doc-b"],
            metadata={"intended_split": "plan_execute should beat react"},
        )
        records = [
            _record("cg_rag_split", "react", False, "retrieval_qa", unsupported=True),
            _record("cg_rag_split", "plan_execute", True, "retrieval_qa"),
        ]

        markdown = "\n".join(build_case_cards(records, [case], run_path="reports/example.jsonl", max_cards=1))

        self.assertIn("# Representative Case Cards", markdown)
        self.assertIn("cg_rag_split", markdown)
        self.assertIn("retrieval_depth", markdown)
        self.assertIn("plan_execute", markdown)
        self.assertIn("react", markdown)
        self.assertIn("What this demonstrates", markdown)


def _record(
    case_id: str,
    strategy: str,
    success: bool,
    family: str,
    cost: float = 1.0,
    context: int = 120,
    unsupported: bool = False,
    budget: bool = False,
) -> dict:
    """Build a minimal raw run record for report tests."""

    return {
        "case_id": case_id,
        "strategy": strategy,
        "success": success,
        "family": family,
        "cost_proxy": cost,
        "context_chars_used": context,
        "tool_calls": [
            {"tool_name": "search_docs", "arguments": {"top_k": 1}, "result": {"doc_ids": ["doc-a"]}}
        ],
        "grader_result": {
            "unsupported_answer": unsupported,
            "budget_violation": budget,
            "citation_coverage": 0.5 if unsupported else 1.0,
            "reason": "gold documents retrieved" if success else "missing required gold documents or budget exceeded",
        },
    }


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the case-card tests and verify the expected failure**

Run:

```powershell
python -m unittest tests.test_case_cards_report
```

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.generate_case_cards'`.

- [ ] **Step 3: Commit the failing tests**

Run:

```powershell
git -c core.excludesfile= add tests/test_case_cards_report.py
git -c core.excludesfile= commit -m "test: add case card report expectations"
```

Expected: commit succeeds and records only `tests/test_case_cards_report.py`.

---

### Task 2: Implement `generate_case_cards.py`

**Files:**
- Create: `scripts/generate_case_cards.py`
- Test: `tests/test_case_cards_report.py`

- [ ] **Step 1: Create the case-card generator**

Create `scripts/generate_case_cards.py` with this exact content:

```python
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
        "| strategy | success | tools | cost | context | unsupported | budget_violation | grader_reason |",
        "|---|---:|---|---:|---:|---:|---:|---|",
    ]
    for row in _sorted_rows(rows):
        grader_result = row.get("grader_result") or {}
        lines.append(
            "| "
            f"{_escape(row.get('strategy'))} | "
            f"{row.get('success')} | "
            f"{_escape(_tool_sequence(row))} | "
            f"{float(row.get('cost_proxy') or 0.0):.3f} | "
            f"{int(row.get('context_chars_used') or 0)} | "
            f"{grader_result.get('unsupported_answer', False)} | "
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
```

- [ ] **Step 2: Run the focused case-card tests**

Run:

```powershell
python -m unittest tests.test_case_cards_report
```

Expected: PASS with 2 tests.

- [ ] **Step 3: Run compile smoke for the new script**

Run:

```powershell
python -m compileall -q scripts/generate_case_cards.py tests/test_case_cards_report.py
```

Expected: no output and exit code 0.

- [ ] **Step 4: Commit the case-card generator**

Run:

```powershell
git -c core.excludesfile= add scripts/generate_case_cards.py tests/test_case_cards_report.py
git -c core.excludesfile= commit -m "feat: add case card generator"
```

Expected: commit succeeds and includes the generator plus its tests.

---

### Task 3: Add failing tests for the context-budget frontier report

**Files:**
- Create: `tests/test_frontier_report.py`
- Later implementation target: `scripts/generate_frontier_report.py`

- [ ] **Step 1: Write the failing frontier tests**

Create `tests/test_frontier_report.py` with this exact content:

```python
"""Tests for success-cost frontier report generation."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.generate_frontier_report import build_frontier_report, dominated_strategies, strategy_points


class FrontierReportTest(unittest.TestCase):
    """Frontier report unit tests."""

    def test_dominated_strategies_detects_success_cost_dominance(self) -> None:
        """A lower-success same-cost strategy should be dominated."""

        points = [
            {"strategy": "react", "success_rate": 0.50, "mean_cost": 1.0, "mean_context": 100.0, "budget_rate": 0.0},
            {"strategy": "context_budget", "success_rate": 0.75, "mean_cost": 1.0, "mean_context": 90.0, "budget_rate": 0.0},
            {"strategy": "verify_then_answer", "success_rate": 0.75, "mean_cost": 2.0, "mean_context": 95.0, "budget_rate": 0.0},
        ]

        dominated = dominated_strategies(points)

        self.assertIn("react", dominated)
        self.assertIn("verify_then_answer", dominated)
        self.assertNotIn("context_budget", dominated)

    def test_strategy_points_and_markdown_include_context_budget_focus(self) -> None:
        """The report should summarize strategies and explain context_budget splits."""

        records = [
            _record("case-1", "react", False, 1.0, 100),
            _record("case-1", "context_budget", True, 1.1, 90),
            _record("case-1", "verify_then_answer", True, 2.0, 120),
            _record("case-2", "react", True, 0.8, 80),
            _record("case-2", "context_budget", False, 0.7, 60, unsupported=True),
            _record("case-2", "verify_then_answer", True, 2.0, 110),
        ]

        points = strategy_points(records)
        markdown = "\n".join(build_frontier_report(records, run_path="reports/example.jsonl"))

        self.assertEqual({point["strategy"] for point in points}, {"react", "context_budget", "verify_then_answer"})
        self.assertIn("# Context Budget Frontier", markdown)
        self.assertIn("context_budget", markdown)
        self.assertIn("Success-Cost Table", markdown)
        self.assertIn("Context Budget Focus", markdown)
        self.assertIn("case-1", markdown)
        self.assertIn("case-2", markdown)


def _record(
    case_id: str,
    strategy: str,
    success: bool,
    cost: float,
    context: int,
    unsupported: bool = False,
) -> dict:
    """Build a minimal raw run record for frontier tests."""

    return {
        "case_id": case_id,
        "strategy": strategy,
        "success": success,
        "family": "retrieval_qa",
        "cost_proxy": cost,
        "context_chars_used": context,
        "tool_calls": [{"tool_name": "search_docs", "latency_ms": 0}],
        "grader_result": {
            "unsupported_answer": unsupported,
            "budget_violation": False,
            "citation_coverage": 0.0 if unsupported else 1.0,
            "reason": "gold documents retrieved" if success else "missing required gold documents or budget exceeded",
        },
    }


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the frontier tests and verify the expected failure**

Run:

```powershell
python -m unittest tests.test_frontier_report
```

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.generate_frontier_report'`.

- [ ] **Step 3: Commit the failing frontier tests**

Run:

```powershell
git -c core.excludesfile= add tests/test_frontier_report.py
git -c core.excludesfile= commit -m "test: add frontier report expectations"
```

Expected: commit succeeds and records only `tests/test_frontier_report.py`.

---

### Task 4: Implement `generate_frontier_report.py`

**Files:**
- Create: `scripts/generate_frontier_report.py`
- Test: `tests/test_frontier_report.py`

- [ ] **Step 1: Create the frontier generator**

Create `scripts/generate_frontier_report.py` with this exact content:

```python
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

    overall = summarize(records)
    points = strategy_points(records)
    dominated = dominated_strategies(points)
    lines = [
        "# Context Budget Frontier",
        "",
        "> Seed-suite success-cost view for deterministic MVP strategies.",
        "",
        "## Overview",
        "",
        f"- Source run trace: `{run_path}`",
        f"- Run records: {int(overall['case_count'])}",
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
    lines.extend(_context_budget_focus(records))
    lines.extend([
        "",
        "## Next Policy Upgrade",
        "",
        "The next algorithm-signal milestone is an explicit Value-of-Information policy:",
        "",
        "```text",
        "chunk_value = query_relevance * source_reliability * novelty",
        "chunk_cost = estimated_context_chars + tool_cost",
        "selection_score = chunk_value / max(chunk_cost, 1)",
        "```",
        "",
        "This frontier report should remain the comparison surface after the policy upgrade.",
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


def _format_case_list(case_ids: list[str]) -> str:
    """Format case ids for a Markdown bullet."""

    if not case_ids:
        return "none"
    return ", ".join(f"`{case_id}`" for case_id in case_ids)


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
```

- [ ] **Step 2: Run the focused frontier tests**

Run:

```powershell
python -m unittest tests.test_frontier_report
```

Expected: PASS with 2 tests.

- [ ] **Step 3: Run the combined focused report tests**

Run:

```powershell
python -m unittest tests.test_case_cards_report tests.test_frontier_report
```

Expected: PASS with 4 tests.

- [ ] **Step 4: Run compile smoke for both report scripts**

Run:

```powershell
python -m compileall -q scripts/generate_case_cards.py scripts/generate_frontier_report.py tests/test_case_cards_report.py tests/test_frontier_report.py
```

Expected: no output and exit code 0.

- [ ] **Step 5: Commit the frontier generator**

Run:

```powershell
git -c core.excludesfile= add scripts/generate_frontier_report.py tests/test_frontier_report.py
git -c core.excludesfile= commit -m "feat: add context budget frontier report"
```

Expected: commit succeeds and includes the generator plus its tests.

---

### Task 5: Generate showcase artifacts and add README/report-index checks

**Files:**
- Create: `tests/test_showcase_docs.py`
- Generate: `reports/case_cards.md`
- Generate: `reports/context_budget_frontier.md`
- Modify: `README.md`
- Modify: `reports/README.md`

- [ ] **Step 1: Write failing documentation checks**

Create `tests/test_showcase_docs.py` with this exact content:

```python
"""Tests for reviewer-facing showcase links."""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class ShowcaseDocsTest(unittest.TestCase):
    """Documentation link checks for generated showcase artifacts."""

    def test_readme_links_claims_to_evidence(self) -> None:
        """README should expose a compact claim-evidence map."""

        text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Claim-Evidence Map", text)
        self.assertIn("reports/agent_strategy_ablation.md", text)
        self.assertIn("reports/case_cards.md", text)
        self.assertIn("reports/context_budget_frontier.md", text)
        self.assertIn("reports/tool_manifest.json", text)

    def test_reports_index_lists_generated_showcase_artifacts(self) -> None:
        """Reports index should list new generated artifacts and commands."""

        text = (REPO_ROOT / "reports" / "README.md").read_text(encoding="utf-8")

        self.assertIn("case_cards.md", text)
        self.assertIn("context_budget_frontier.md", text)
        self.assertIn("generate_case_cards.py", text)
        self.assertIn("generate_frontier_report.py", text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run documentation checks and verify the expected failure**

Run:

```powershell
python -m unittest tests.test_showcase_docs
```

Expected: FAIL because README and reports index do not yet include the new showcase links.

- [ ] **Step 3: Regenerate the seed-suite ablation inputs**

Run:

```powershell
python scripts/run_eval.py --strategies react,plan_execute,verify_then_answer,context_budget --out reports/agent_strategy_ablation.jsonl
python scripts/generate_report.py --run reports/agent_strategy_ablation.jsonl --out reports/agent_strategy_ablation.md
```

Expected:

```text
wrote 36 records to reports/agent_strategy_ablation.jsonl
wrote report to reports/agent_strategy_ablation.md
```

- [ ] **Step 4: Generate the new showcase artifacts**

Run:

```powershell
python scripts/generate_case_cards.py --run reports/agent_strategy_ablation.jsonl --cases data/benchmark/cases.sample.jsonl --out reports/case_cards.md
python scripts/generate_frontier_report.py --run reports/agent_strategy_ablation.jsonl --out reports/context_budget_frontier.md
```

Expected:

```text
wrote case cards to reports/case_cards.md
wrote frontier report to reports/context_budget_frontier.md
```

- [ ] **Step 5: Update README with the claim-evidence map**

Insert this section after the `## What It Shows` table and before `## 3-Minute Run` in `README.md`:

```markdown
## Claim-Evidence Map

| Claim | Evidence Artifact |
|---|---|
| Same cases compare multiple deterministic agent strategies. | `reports/agent_strategy_ablation.md`, `reports/agent_strategy_ablation.jsonl` |
| Tool use is exposed through an MCP-compatible in-process boundary. | `reports/tool_manifest.json`, `src/contextguard_agent_lab/tools/registry.py` |
| Independent grading is stored separately from agent answers. | `grader_result` fields in `reports/agent_strategy_ablation.jsonl` |
| Context and budget tradeoffs are measurable. | `reports/context_budget_frontier.md`, `reports/agent_strategy_ablation.md` |
| Representative strategy splits are inspectable. | `reports/case_cards.md` |
```

- [ ] **Step 6: Update the artifact table in `reports/README.md`**

Replace the existing artifact table with this table:

```markdown
| Artifact | Purpose | Status |
|---|---|---|
| `sample_report.md` | Starter smoke report across MVP strategies. | Generated. |
| `sample_run.jsonl` | Full structured smoke run records. | Generated. |
| `tool_manifest.json` | MCP-compatible tool contract manifest. | Generated by `scripts/export_tool_manifest.py`. |
| `agent_strategy_ablation.md` | Seed-suite by-strategy / by-family report with observed splits and success-cost view. | Generated. |
| `agent_strategy_ablation.jsonl` | Full seed-suite run records across the four MVP strategies. | Generated. |
| `case_cards.md` | Representative strategy-split case cards for reviewer inspection. | Generated by `scripts/generate_case_cards.py`. |
| `context_budget_frontier.md` | Seed-suite success-cost frontier and context-budget focus report. | Generated by `scripts/generate_frontier_report.py`. |
| Optional static showcase | Lightweight static page if Markdown artifacts become insufficient. | Planned. |
```

- [ ] **Step 7: Update regeneration commands in `reports/README.md`**

After the seed-suite ablation command block, add this block:

````markdown
Generate showcase artifacts from the seed-suite ablation:

```powershell
python scripts/generate_case_cards.py --run reports/agent_strategy_ablation.jsonl --cases data/benchmark/cases.sample.jsonl --out reports/case_cards.md
python scripts/generate_frontier_report.py --run reports/agent_strategy_ablation.jsonl --out reports/context_budget_frontier.md
```
````

- [ ] **Step 8: Run documentation checks again**

Run:

```powershell
python -m unittest tests.test_showcase_docs
```

Expected: PASS with 2 tests.

- [ ] **Step 9: Inspect generated artifact headers**

Run:

```powershell
Get-Content -LiteralPath reports/case_cards.md -TotalCount 80
Get-Content -LiteralPath reports/context_budget_frontier.md -TotalCount 80
```

Expected:

- `reports/case_cards.md` starts with `# Representative Case Cards`.
- `reports/context_budget_frontier.md` starts with `# Context Budget Frontier`.
- Both files reference `reports/agent_strategy_ablation.jsonl`.

- [ ] **Step 10: Commit generated artifacts and docs**

Run:

```powershell
git -c core.excludesfile= add README.md reports/README.md reports/case_cards.md reports/context_budget_frontier.md reports/agent_strategy_ablation.jsonl reports/agent_strategy_ablation.md tests/test_showcase_docs.py
git -c core.excludesfile= commit -m "docs: add showcase evidence artifacts"
```

Expected: commit succeeds and includes README, reports index, generated showcase artifacts, refreshed ablation artifacts, and docs checks.

---

### Task 6: Full validation and closeout

**Files:**
- Validate: `src/`, `scripts/`, `tests/`, `reports/`, `README.md`

- [ ] **Step 1: Run compile validation**

Run:

```powershell
python -m compileall -q src scripts tests
```

Expected: no output and exit code 0.

- [ ] **Step 2: Run all unit tests**

Run:

```powershell
python -m unittest discover -s tests
```

Expected: all tests pass. Expected count after this plan is at least 17 tests.

- [ ] **Step 3: Regenerate smoke artifacts**

Run:

```powershell
python scripts/run_eval.py --case-limit 3 --strategies react,plan_execute,verify_then_answer,context_budget --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
python scripts/export_tool_manifest.py --out reports/tool_manifest.json
```

Expected:

```text
wrote 12 records to reports/sample_run.jsonl
wrote report to reports/sample_report.md
wrote tool manifest to reports/tool_manifest.json
```

- [ ] **Step 4: Regenerate seed-suite showcase artifacts**

Run:

```powershell
python scripts/run_eval.py --strategies react,plan_execute,verify_then_answer,context_budget --out reports/agent_strategy_ablation.jsonl
python scripts/generate_report.py --run reports/agent_strategy_ablation.jsonl --out reports/agent_strategy_ablation.md
python scripts/generate_case_cards.py --run reports/agent_strategy_ablation.jsonl --cases data/benchmark/cases.sample.jsonl --out reports/case_cards.md
python scripts/generate_frontier_report.py --run reports/agent_strategy_ablation.jsonl --out reports/context_budget_frontier.md
```

Expected:

```text
wrote 36 records to reports/agent_strategy_ablation.jsonl
wrote report to reports/agent_strategy_ablation.md
wrote case cards to reports/case_cards.md
wrote frontier report to reports/context_budget_frontier.md
```

- [ ] **Step 5: Re-run all tests after regeneration**

Run:

```powershell
python -m unittest discover -s tests
```

Expected: all tests pass.

- [ ] **Step 6: Check git status**

Run:

```powershell
git -c core.excludesfile= status --short
```

Expected: no output. If regenerated files changed, inspect the diff, commit deterministic generated changes with:

```powershell
git -c core.excludesfile= add reports/sample_run.jsonl reports/sample_report.md reports/tool_manifest.json reports/agent_strategy_ablation.jsonl reports/agent_strategy_ablation.md reports/case_cards.md reports/context_budget_frontier.md
git -c core.excludesfile= commit -m "chore: refresh showcase reports"
```

- [ ] **Step 7: Produce closeout summary**

Report these items to the user:

- Files created.
- Files modified.
- Commands run and pass/fail results.
- Generated artifact paths.
- Commit hashes.
- Whether working tree is clean.
- Whether push happened. Expected answer: local commits only unless user explicitly approves push.

---

## Self-Review

### Spec coverage

- `scripts/generate_case_cards.py`: Task 1 and Task 2.
- `scripts/generate_frontier_report.py`: Task 3 and Task 4.
- `reports/case_cards.md`: Task 5 Step 4.
- `reports/context_budget_frontier.md`: Task 5 Step 4.
- `README.md` claim-evidence map: Task 5 Step 5.
- `reports/README.md` artifact index and commands: Task 5 Step 6 and Step 7.
- Deterministic tests: Task 1, Task 3, Task 5.
- Default validation and generation commands: Task 6.

### Completeness scan

All file paths, commands, expected outputs, and code contents are explicit.

### Type consistency

- `select_representative_cases(records, cases, max_cards)` is imported and tested before being defined in `scripts/generate_case_cards.py`.
- `build_case_cards(records, cases, run_path, max_cards)` is imported and tested before being defined in `scripts/generate_case_cards.py`.
- `strategy_points(records)`, `dominated_strategies(points)`, and `build_frontier_report(records, run_path)` are imported and tested before being defined in `scripts/generate_frontier_report.py`.
- Raw run-record dictionary keys match existing JSONL structure: `case_id`, `strategy`, `success`, `family`, `cost_proxy`, `context_chars_used`, `tool_calls`, and `grader_result`.
