"""Tests for benchmark schema contracts."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from contextguard_agent_lab.benchmark.schema import BudgetSpec, CaseSpec, ExpectedOutcome, GraderSpec


class SchemaContractsTest(unittest.TestCase):
    """Benchmark schema unit tests."""

    def test_case_spec_normalizes_nested_dicts(self) -> None:
        """JSON-loaded nested contracts should become typed dataclasses."""

        case = CaseSpec(
            case_id="case-1",
            case_type="rag_qa",
            user_query="question",
            expected_answer="answer",
            gold_doc_ids=["doc-1"],
            budget={"max_tool_calls": 2, "max_context_chars": 100},
            expected_outcome={"answer": "answer", "gold_doc_ids": ["doc-1"]},
            grader={"grader_type": "retrieval_qa", "require_citation": True},
        )

        self.assertIsInstance(case.budget, BudgetSpec)
        self.assertIsInstance(case.expected_outcome, ExpectedOutcome)
        self.assertIsInstance(case.grader, GraderSpec)
        self.assertEqual(case.family, "retrieval_qa")
        self.assertEqual(case.budget.max_tool_calls, 2)

    def test_case_spec_derives_legacy_expected_outcome(self) -> None:
        """Legacy sample cases should still expose expected outcome fields."""

        case = CaseSpec(
            case_id="case-sensitive",
            case_type="sensitive_action",
            user_query="export data",
            expected_answer="block",
            required_evidence=["user_authorization"],
            sensitive_action="export_data",
        )

        self.assertEqual(case.family, "sensitive_action")
        self.assertEqual(case.expected_outcome.sensitive_decision, "block")


if __name__ == "__main__":
    unittest.main()
