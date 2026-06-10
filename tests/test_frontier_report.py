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
            _record(
                "case-1",
                "context_budget",
                True,
                1.1,
                90,
                selection_reasons=[
                    {"doc_id": "doc-good", "selected": True, "skipped_reason": ""},
                    {"doc_id": "doc-noisy", "selected": False, "skipped_reason": "lower_source_reliability"},
                ],
            ),
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
        self.assertIn("Selection Trace Samples", markdown)
        self.assertIn("doc-good", markdown)
        self.assertIn("case-1", markdown)
        self.assertIn("case-2", markdown)


def _record(
    case_id: str,
    strategy: str,
    success: bool,
    cost: float,
    context: int,
    unsupported: bool = False,
    selection_reasons: list[dict] | None = None,
) -> dict:
    """Build a minimal raw run record for frontier tests."""

    return {
        "case_id": case_id,
        "strategy": strategy,
        "success": success,
        "family": "retrieval_qa",
        "cost_proxy": cost,
        "context_chars_used": context,
        "metrics": {"selection_reasons": selection_reasons or []},
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
