"""Shared builders for the default benchmark tool registry."""

from __future__ import annotations

from pathlib import Path

from contextguard_agent_lab.tools.registry import ToolExecutor, ToolRegistry, ToolSpec
from contextguard_agent_lab.tools.retrieval import InMemoryRetriever, verify_citation


def build_default_tool_registry(repo_root: str | Path) -> ToolRegistry:
    """Build the runtime registry used by eval and manifest export."""

    root = Path(repo_root)
    retriever = InMemoryRetriever.from_jsonl(root / "data" / "corpus" / "docs.sample.jsonl")
    registry = ToolRegistry()
    registry.register(
        "search_docs",
        retriever.search_docs,
        ToolSpec(
            name="search_docs",
            description="Search public toy corpus documents by keyword overlap.",
            input_schema={
                "type": "object",
                "properties": {"query": {"type": "string"}, "top_k": {"type": "integer"}},
                "required": ["query"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "doc_ids": {"type": "array"},
                    "chunks": {"type": "array"},
                    "answer_hint": {"type": "string"},
                },
            },
            risk_level="low",
            side_effect="none",
            cost_estimate=1.0,
            mcp_exposure="manifest",
        ),
    )
    registry.register(
        "verify_citation",
        verify_citation,
        ToolSpec(
            name="verify_citation",
            description="Check whether an answer is grounded in trusted retrieved evidence.",
            input_schema={
                "type": "object",
                "properties": {
                    "answer": {"type": "string"},
                    "chunks": {"type": "array"},
                    "answer_source_doc_ids": {"type": "array"},
                },
                "required": ["answer", "chunks", "answer_source_doc_ids"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "supported": {"type": "boolean"},
                    "grounded": {"type": "boolean"},
                    "trusted_source": {"type": "boolean"},
                    "citation_coverage": {"type": "number"},
                },
            },
            risk_level="low",
            side_effect="none",
            cost_estimate=1.5,
            mcp_exposure="manifest",
        ),
    )
    return registry


def build_default_tool_executor(repo_root: str | Path) -> ToolExecutor:
    """Build the default ToolExecutor for the benchmark runner."""

    return ToolExecutor(build_default_tool_registry(repo_root))
