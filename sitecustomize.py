"""Local source-layout import helper.

This keeps `python -m unittest discover -s tests` working from a fresh clone
without requiring an editable install first.
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "src"
if SRC.exists():
    sys.path.insert(0, str(SRC))
