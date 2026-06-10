"""Tests for ToolSpec, ToolExecutor, and manifest export."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from contextguard_agent_lab.tools.registry import ToolExecutor, ToolRegistry, ToolSpec, export_tool_manifest
from contextguard_agent_lab.mcp_server.server import build_tool_manifest


class ToolBoundaryTest(unittest.TestCase):
    """Tool boundary unit tests."""

    def test_manifest_exports_mcp_compatible_fields(self) -> None:
        """Manifest entries should include schema, risk, cost, and exposure metadata."""

        registry = ToolRegistry()
        registry.register(
            "echo",
            lambda arguments: {"text": arguments["text"]},
            ToolSpec(
                name="echo",
                description="Echo text.",
                input_schema={"type": "object", "required": ["text"]},
                output_schema={"type": "object", "required": ["text"]},
                risk_level="low",
                side_effect="none",
                cost_estimate=0.5,
                mcp_exposure="manifest",
            ),
        )

        manifest = export_tool_manifest(registry)
        self.assertEqual(manifest[0]["name"], "echo")
        self.assertIn("input_schema", manifest[0])
        self.assertEqual(manifest[0]["cost_estimate"], 0.5)

    def test_executor_records_context_and_cost(self) -> None:
        """Executor results should carry trace accounting metadata."""

        registry = ToolRegistry()
        registry.register(
            "echo",
            lambda arguments: {"text": arguments["text"]},
            ToolSpec(
                name="echo",
                description="Echo text.",
                input_schema={"type": "object"},
                output_schema={"type": "object"},
                cost_estimate=0.5,
            ),
        )
        result = ToolExecutor(registry).call("echo", {"text": "hello"})
        trace = result.trace("case-1", 1)

        self.assertGreaterEqual(trace.context_chars, 5)
        self.assertGreater(trace.cost_proxy, 0.5)
        self.assertEqual(trace.risk_level, "low")

    def test_mcp_manifest_helper_returns_full_contracts(self) -> None:
        """MCP manifest helper should expose more than tool names."""

        manifest = build_tool_manifest()
        search_docs = next(entry for entry in manifest if entry["name"] == "search_docs")

        self.assertIn("input_schema", search_docs)
        self.assertIn("output_schema", search_docs)
        self.assertIn("properties", search_docs["input_schema"])
        self.assertIn("allowed_doc_ids", search_docs["input_schema"]["properties"])
        self.assertIn("mcp_exposure", search_docs)
        self.assertEqual(search_docs["side_effect"], "none")
        verify = next(entry for entry in manifest if entry["name"] == "verify_citation")
        self.assertIn("answer_source_doc_ids", verify["input_schema"]["properties"])
        self.assertNotIn("expected_doc_ids", verify["input_schema"]["properties"])
        export = next(entry for entry in manifest if entry["name"] == "export_data")
        self.assertEqual(export["risk_level"], "high")
        self.assertEqual(export["side_effect"], "simulated_sensitive_action")
        self.assertIn("observed_evidence", export["input_schema"]["properties"])


if __name__ == "__main__":
    unittest.main()
