"""JSONL loaders for benchmark cases."""

from __future__ import annotations

import json
from pathlib import Path

from .schema import CaseSpec


def load_cases(path: str | Path) -> list[CaseSpec]:
    """Load CaseSpec records from JSONL."""

    cases: list[CaseSpec] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        cases.append(CaseSpec(**json.loads(line)))
    return cases
