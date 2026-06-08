"""Generate a starter Markdown report from JSONL run records."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from contextguard_agent_lab.trace.jsonl import read_run_records


def main() -> None:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--run", default="reports/sample_run.jsonl")
    parser.add_argument("--out", default="reports/sample_report.md")
    args = parser.parse_args()

    records = read_run_records(REPO_ROOT / args.run)
    success_count = sum(1 for record in records if record.get("success"))
    lines = [
        "# Sample Agent Evaluation Report",
        "",
        f"- Cases: {len(records)}",
        f"- Success: {success_count}",
        "",
        "| case_id | strategy | success | answer |",
        "|---|---|---:|---|",
    ]
    for record in records:
        answer = str(record.get("answer", "")).replace("|", "/")
        lines.append(f"| {record.get('case_id')} | {record.get('strategy')} | {record.get('success')} | {answer} |")
    target = REPO_ROOT / args.out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote report to {args.out}")


if __name__ == "__main__":
    main()
