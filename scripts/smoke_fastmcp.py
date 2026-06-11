"""Smoke-test the FastMCP server for search_docs and verify_citation."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from contextguard_agent_lab.mcp_server.server import get_mcp_server


async def _run_smoke(query: str) -> dict:
    """Call the two demonstrated FastMCP tools in-process."""

    try:
        from fastmcp import Client
    except ImportError as exc:
        raise SystemExit("fastmcp is not installed; install with: pip install -e '.[mcp]'") from exc

    server = get_mcp_server(REPO_ROOT)
    async with Client(server) as client:
        tools = await client.list_tools()
        tool_names = sorted(tool.name for tool in tools)
        search = await client.call_tool("search_docs", {"query": query, "top_k": 2})
        chunks = search.data.get("chunks", []) if search.data else []
        answer = " ".join(str(chunk.get("text", "")) for chunk in chunks[:1]) or "No answer found."
        source_ids = [str(chunk.get("doc_id")) for chunk in chunks[:1] if chunk.get("doc_id")]
        verify = await client.call_tool(
            "verify_citation",
            {
                "answer": answer,
                "chunks": chunks,
                "answer_source_doc_ids": source_ids,
            },
        )
        return {
            "tools": tool_names,
            "search_doc_ids": search.data.get("doc_ids", []) if search.data else [],
            "verify_supported": verify.data.get("supported") if verify.data else None,
            "verify_grounded": verify.data.get("grounded") if verify.data else None,
        }


def main() -> None:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="MCP retrieval tool")
    args = parser.parse_args()
    result = asyncio.run(_run_smoke(args.query))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
