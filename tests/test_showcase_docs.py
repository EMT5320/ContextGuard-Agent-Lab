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
