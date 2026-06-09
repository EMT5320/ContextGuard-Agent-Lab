"""MCP-compatible manifest helpers.

FastMCP integration is a full-target artifact. The MVP exposes concrete
tool contracts through an in-process manifest first.
"""

from __future__ import annotations

from typing import Any

from contextguard_agent_lab.tools.registry import ToolRegistry, ToolSpec


def build_tool_manifest() -> list[dict[str, Any]]:
    """Return the public tool contracts planned for MCP exposure."""

    registry = ToolRegistry()
    registry.register(
        "search_docs",
        lambda _arguments: {},
        ToolSpec(
            name="search_docs",
            description="Search public toy corpus documents.",
            input_schema={"type": "object", "required": ["query"]},
            output_schema={"type": "object", "required": ["doc_ids", "chunks"]},
            risk_level="low",
            side_effect="none",
            cost_estimate=1.0,
            mcp_exposure="manifest",
        ),
    )
    registry.register(
        "verify_citation",
        lambda _arguments: {},
        ToolSpec(
            name="verify_citation",
            description="Check whether a final answer is supported by retrieved evidence.",
            input_schema={"type": "object", "required": ["answer", "doc_ids"]},
            output_schema={"type": "object", "required": ["supported", "citation_coverage"]},
            risk_level="low",
            side_effect="none",
            cost_estimate=1.5,
            mcp_exposure="manifest",
        ),
    )
    return registry.export_tool_manifest()
