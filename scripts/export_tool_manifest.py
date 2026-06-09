"""Export the starter MCP-compatible tool manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from contextguard_agent_lab.mcp_server.server import build_tool_manifest


def main() -> None:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="reports/tool_manifest.json")
    args = parser.parse_args()

    target = REPO_ROOT / args.out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(build_tool_manifest(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote tool manifest to {args.out}")


if __name__ == "__main__":
    main()
