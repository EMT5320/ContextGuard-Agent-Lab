"""Tests for FastMCP server exposure of core retrieval tools."""

import asyncio
import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

if importlib.util.find_spec("fastmcp") is None:
    raise unittest.SkipTest("fastmcp is not installed")

from fastmcp import Client

from contextguard_agent_lab.mcp_server.server import build_tool_manifest, get_mcp_server


class FastMCPServerTest(unittest.TestCase):
    """FastMCP integration tests."""

    def test_manifest_marks_fastmcp_tools(self) -> None:
        """search_docs and verify_citation should be marked as FastMCP-exposed."""

        manifest = build_tool_manifest()
        search_docs = next(entry for entry in manifest if entry["name"] == "search_docs")
        verify = next(entry for entry in manifest if entry["name"] == "verify_citation")
        export = next(entry for entry in manifest if entry["name"] == "export_data")

        self.assertEqual(search_docs["mcp_exposure"], "fastmcp")
        self.assertEqual(verify["mcp_exposure"], "fastmcp")
        self.assertEqual(export["mcp_exposure"], "manifest")

    def test_fastmcp_tools_are_callable(self) -> None:
        """FastMCP should expose and execute the two demonstrated tools."""

        async def exercise() -> dict:
            server = get_mcp_server()
            async with Client(server) as client:
                tools = await client.list_tools()
                names = {tool.name for tool in tools}
                search = await client.call_tool("search_docs", {"query": "MCP retrieval", "top_k": 1})
                chunks = search.data["chunks"]
                answer = chunks[0]["text"]
                verify = await client.call_tool(
                    "verify_citation",
                    {
                        "answer": answer,
                        "chunks": chunks,
                        "answer_source_doc_ids": [chunks[0]["doc_id"]],
                    },
                )
                return {
                    "tool_names": names,
                    "doc_ids": search.data["doc_ids"],
                    "supported": verify.data["supported"],
                }

        result = asyncio.run(exercise())
        self.assertEqual(result["tool_names"], {"search_docs", "verify_citation"})
        self.assertTrue(result["doc_ids"])
        self.assertTrue(result["supported"])


if __name__ == "__main__":
    unittest.main()
