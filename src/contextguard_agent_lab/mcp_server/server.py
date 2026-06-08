"""MCP server manifest placeholder.

FastMCP integration is planned for milestone W2. The first scaffold
exposes the same tool names through an in-process registry so tests stay
dependency-free.
"""

from __future__ import annotations


def build_tool_manifest() -> list[dict[str, str]]:
    """Return the public tool names planned for MCP exposure."""

    return [
        {"name": "search_docs", "category": "retrieval"},
        {"name": "read_doc", "category": "retrieval"},
        {"name": "verify_citation", "category": "retrieval"},
        {"name": "list_files", "category": "workspace"},
        {"name": "read_file", "category": "workspace"},
        {"name": "apply_patch", "category": "workspace"},
        {"name": "run_tests", "category": "workspace"},
        {"name": "export_data", "category": "sensitive"},
    ]
