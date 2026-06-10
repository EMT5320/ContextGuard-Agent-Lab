"""MCP-compatible manifest helpers.

FastMCP integration is a full-target artifact. The MVP exposes concrete
tool contracts through an in-process manifest first.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from contextguard_agent_lab.tools.factory import build_default_tool_registry


def build_tool_manifest(repo_root: str | Path | None = None) -> list[dict[str, Any]]:
    """Return the public tool contracts planned for MCP exposure."""

    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[3]
    registry = build_default_tool_registry(root)
    return registry.export_tool_manifest()
