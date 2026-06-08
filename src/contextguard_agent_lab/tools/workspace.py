"""Workspace tools for coding-agent-like tasks.

The tools are path-bounded. They are intentionally conservative because
this portfolio project should demonstrate safe local-agent design.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class WorkspaceTools:
    """Path-bounded file tools for toy code repair tasks."""

    def __init__(self, workspace_root: str | Path) -> None:
        self.workspace_root = Path(workspace_root).resolve()

    def _resolve(self, relative_path: str) -> Path:
        """Resolve a path and keep it inside the workspace root."""

        target = (self.workspace_root / relative_path).resolve()
        if self.workspace_root not in target.parents and target != self.workspace_root:
            raise ValueError(f"Path escapes workspace: {relative_path}")
        return target

    def list_files(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """List files below a relative directory."""

        rel = str(arguments.get("path", "."))
        target = self._resolve(rel)
        files = [str(path.relative_to(self.workspace_root)) for path in target.rglob("*") if path.is_file()]
        return {"files": files}

    def read_file(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Read a UTF-8 file inside the workspace."""

        target = self._resolve(str(arguments["path"]))
        return {"path": str(target.relative_to(self.workspace_root)), "text": target.read_text(encoding="utf-8")}
