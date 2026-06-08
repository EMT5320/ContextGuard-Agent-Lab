"""Toy retrieval tools used by the first milestone."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class InMemoryRetriever:
    """Small keyword retriever for deterministic tests and demos."""

    def __init__(self, docs: list[dict[str, str]]) -> None:
        self.docs = docs

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "InMemoryRetriever":
        """Load document rows from JSONL."""

        docs: list[dict[str, str]] = []
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if line.strip():
                docs.append(json.loads(line))
        return cls(docs)

    def search_docs(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Search by simple token overlap and return answer hints."""

        query = str(arguments.get("query", "")).lower()
        top_k = int(arguments.get("top_k", 3))
        scored: list[tuple[int, dict[str, str]]] = []
        for doc in self.docs:
            text = (doc.get("title", "") + " " + doc.get("text", "")).lower()
            score = sum(1 for token in query.split() if token in text)
            scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        selected = [doc for score, doc in scored[:top_k] if score > 0]
        if not selected and self.docs:
            selected = [self.docs[0]]
        return {
            "doc_ids": [doc["doc_id"] for doc in selected],
            "chunks": selected,
            "answer_hint": selected[0].get("text", "") if selected else "",
        }
