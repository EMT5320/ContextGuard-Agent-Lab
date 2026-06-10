"""Toy retrieval tools used by the first milestone."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class InMemoryRetriever:
    """Small keyword retriever for deterministic tests and demos."""

    def __init__(self, docs: list[dict[str, Any]]) -> None:
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

        query = str(arguments.get("query", ""))
        query_tokens = _content_tokens(query)
        top_k = int(arguments.get("top_k", 3))
        scored: list[tuple[int, int, dict[str, Any], set[str]]] = []
        for index, doc in enumerate(self.docs):
            text = (doc.get("title", "") + " " + doc.get("text", "")).lower()
            text_tokens = _content_tokens(text)
            matched_tokens = query_tokens.intersection(text_tokens)
            scored.append((len(matched_tokens), index, doc, matched_tokens))
        scored.sort(key=lambda item: (-item[0], item[1]))
        selected = [
            {**doc, "retrieval_score": score, "matched_query_tokens": sorted(matched_tokens)}
            for score, _index, doc, matched_tokens in scored[:top_k]
            if score > 0
        ]
        if not selected and self.docs:
            selected = [{**self.docs[0], "retrieval_score": 0, "matched_query_tokens": []}]
        return {
            "doc_ids": [doc["doc_id"] for doc in selected],
            "chunks": selected,
            "answer_hint": selected[0].get("text", "") if selected else "",
        }


def verify_citation(arguments: dict[str, Any]) -> dict[str, Any]:
    """Check whether an answer is grounded in trusted retrieved evidence."""

    answer = str(arguments.get("answer", ""))
    chunks = [chunk for chunk in arguments.get("chunks", []) if isinstance(chunk, dict)]
    source_ids = {str(doc_id) for doc_id in arguments.get("answer_source_doc_ids", [])}
    source_chunks = [chunk for chunk in chunks if str(chunk.get("doc_id", "")) in source_ids] if source_ids else chunks

    answer_tokens = _content_tokens(answer)
    evidence_text = " ".join(str(chunk.get("text", "")) for chunk in source_chunks)
    evidence_tokens = _content_tokens(evidence_text)
    overlap = (len(answer_tokens.intersection(evidence_tokens)) / len(answer_tokens)) if answer_tokens else 0.0
    grounded = overlap >= 0.5
    trust_score = min((_source_reliability(chunk) for chunk in source_chunks), default=0.0)
    trusted_source = trust_score >= 0.5
    return {
        "supported": grounded and trusted_source,
        "grounded": grounded,
        "trusted_source": trusted_source,
        "citation_coverage": overlap,
        "support_overlap": overlap,
        "source_trust_score": trust_score,
        "answer_source_doc_ids": sorted(source_ids),
    }


def _content_tokens(value: str) -> set[str]:
    """Tokenize content for deterministic overlap checks."""

    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "by",
        "for",
        "in",
        "is",
        "of",
        "or",
        "the",
        "to",
        "what",
        "which",
        "should",
        "must",
        "before",
        "after",
        "with",
    }
    return {token for token in re.findall(r"[a-z0-9_]+", value.lower()) if token not in stop_words}


def _source_reliability(chunk: dict[str, Any]) -> float:
    """Score provenance metadata visible at runtime."""

    if "source_reliability" in chunk:
        try:
            return float(chunk["source_reliability"])
        except (TypeError, ValueError):
            return 0.5
    trust_tier = str(chunk.get("trust_tier", "public")).lower()
    return {
        "official": 1.0,
        "trusted": 0.8,
        "public": 0.6,
        "unverified": 0.2,
    }.get(trust_tier, 0.5)
