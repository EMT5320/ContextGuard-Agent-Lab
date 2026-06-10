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

    def test_source_reliability_cards_explain_provenance_signal(self) -> None:
        """Source-reliability cards should describe the provenance split."""

        case = CaseSpec(
            case_id="cg_trust_split",
            case_type="rag_qa",
            family="source_reliability",
            dimensions=["source_reliability"],
            user_query="Need official source",
            expected_answer="answer",
            gold_doc_ids=["official-doc"],
            metadata={"intended_split": "source-aware strategies should win"},
        )
        records = [
            _record("cg_trust_split", "react", False, "source_reliability", unsupported=True),
            _record("cg_trust_split", "plan_execute", True, "source_reliability"),
        ]

        markdown = "\n".join(build_case_cards(records, [case], run_path="reports/example.jsonl", max_cards=1))

        self.assertIn("Source reliability is visible", markdown)


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
