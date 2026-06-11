"""MCP manifest helpers and FastMCP server for core retrieval tools."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from contextguard_agent_lab.tools.factory import build_default_tool_registry

try:
    from fastmcp import FastMCP
except ImportError:  # pragma: no cover - optional dependency for core unittest path
    FastMCP = None  # type: ignore[assignment,misc]


def repo_root() -> Path:
    """Return the repository root used by benchmark tooling."""

    return Path(__file__).resolve().parents[3]


def build_tool_manifest(repo_root_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Return the public tool contracts planned for MCP exposure."""

    root = Path(repo_root_path) if repo_root_path is not None else repo_root()
    registry = build_default_tool_registry(root)
    return registry.export_tool_manifest()


def _tool_registry(repo_root_path: Path | None = None):
    """Build the shared registry backing both manifest export and FastMCP tools."""

    return build_default_tool_registry(repo_root_path or repo_root())


def build_fastmcp_server(repo_root_path: str | Path | None = None) -> Any:
    """Expose search_docs and verify_citation through a real FastMCP server."""

    if FastMCP is None:
        raise RuntimeError("fastmcp is not installed; install with: pip install -e '.[mcp]'")

    root = Path(repo_root_path) if repo_root_path is not None else repo_root()
    registry = _tool_registry(root)
    mcp = FastMCP("ContextGuard Agent Lab")

    @mcp.tool(
        name="search_docs",
        description="Search public toy corpus documents by keyword overlap.",
    )
    def search_docs(
        query: str,
        top_k: int = 1,
        allowed_doc_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search the toy corpus and return ranked chunks."""

        arguments: dict[str, Any] = {"query": query, "top_k": top_k}
        if allowed_doc_ids:
            arguments["allowed_doc_ids"] = allowed_doc_ids
        return registry.call("search_docs", arguments).payload

    @mcp.tool(
        name="verify_citation",
        description="Check whether an answer is grounded in trusted retrieved evidence.",
    )
    def verify_citation(
        answer: str,
        chunks: list[dict[str, Any]],
        answer_source_doc_ids: list[str],
    ) -> dict[str, Any]:
        """Verify grounding and trust without gold labels."""

        return registry.call(
            "verify_citation",
            {
                "answer": answer,
                "chunks": chunks,
                "answer_source_doc_ids": answer_source_doc_ids,
            },
        ).payload

    return mcp


_mcp_server: Any | None = None


def get_mcp_server(repo_root_path: str | Path | None = None) -> Any:
    """Return a cached FastMCP server for CLI and smoke tests."""

    global _mcp_server
    if repo_root_path is not None:
        return build_fastmcp_server(repo_root_path)
    if _mcp_server is None:
        _mcp_server = build_fastmcp_server()
    return _mcp_server


# Default module-level server object for `fastmcp run` and in-process smoke tests.
mcp = get_mcp_server() if FastMCP is not None else None


if __name__ == "__main__":
    if mcp is None:
        raise SystemExit("fastmcp is not installed; install with: pip install -e '.[mcp]'")
    mcp.run()
