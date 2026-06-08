"""Tests for toy retrieval."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from contextguard_agent_lab.tools.retrieval import InMemoryRetriever


class RetrievalTest(unittest.TestCase):
    """Retrieval unit tests."""

    def test_retriever_returns_matching_doc(self) -> None:
        """Keyword overlap should rank a matching document first."""

        retriever = InMemoryRetriever([
            {"doc_id": "a", "title": "MCP", "text": "search and read tools"},
            {"doc_id": "b", "title": "Other", "text": "unrelated"},
        ])
        result = retriever.search_docs({"query": "MCP search", "top_k": 1})
        self.assertEqual(result["doc_ids"], ["a"])


if __name__ == "__main__":
    unittest.main()

