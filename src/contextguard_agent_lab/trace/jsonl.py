"""JSONL serialization helpers for run records."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from contextguard_agent_lab.benchmark.schema import RunRecord


def write_run_records(path: str | Path, records: list[RunRecord]) -> None:
    """Write run records as JSONL for later report generation."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(asdict(record), ensure_ascii=False) for record in records]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_run_records(path: str | Path) -> list[dict]:
    """Read raw JSONL run records as dictionaries."""

    records: list[dict] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records
