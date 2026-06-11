"""Shared builders for the default benchmark tool registry."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine
from contextguard_agent_lab.tools.registry import ToolExecutor, ToolRegistry, ToolSpec
from contextguard_agent_lab.tools.retrieval import InMemoryRetriever, verify_citation


def build_default_tool_registry(repo_root: str | Path, policy_engine: EvidencePolicyEngine | None = None) -> ToolRegistry:
    """Build the runtime registry used by eval and manifest export."""

    root = Path(repo_root)
    policy = policy_engine or EvidencePolicyEngine.from_json(root / "config" / "policies.json")
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
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer"},
                    "allowed_doc_ids": {"type": "array"},
                },
                "required": ["query"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "doc_ids": {"type": "array"},
                    "chunks": {"type": "array"},
                    "answer_hint": {"type": "string"},
                    "candidate_doc_count": {"type": "integer"},
                },
            },
            risk_level="low",
            side_effect="none",
            cost_estimate=1.0,
            mcp_exposure="fastmcp",
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
            mcp_exposure="fastmcp",
        ),
    )
    registry.register(
        "export_data",
        _export_data_tool(policy),
        ToolSpec(
            name="export_data",
            description="Simulate a high-risk data export decision behind the tool boundary.",
            input_schema={
                "type": "object",
                "properties": {
                    "case_id": {"type": "string"},
                    "action": {"type": "string"},
                    "observed_evidence": {"type": "array"},
                },
                "required": ["case_id", "action", "observed_evidence"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "allowed": {"type": "boolean"},
                    "simulated": {"type": "boolean"},
                    "policy_decision": {"type": "object"},
                },
            },
            risk_level="high",
            side_effect="simulated_sensitive_action",
            cost_estimate=0.5,
            mcp_exposure="manifest",
        ),
    )
    return registry


def build_default_tool_executor(repo_root: str | Path, policy_engine: EvidencePolicyEngine | None = None) -> ToolExecutor:
    """Build the default ToolExecutor for the benchmark runner."""

    return ToolExecutor(build_default_tool_registry(repo_root, policy_engine=policy_engine))


def _export_data_tool(policy_engine: EvidencePolicyEngine):
    """Build a policy-backed simulated sensitive action tool."""

    def call(arguments: dict[str, Any]) -> dict[str, Any]:
        action = str(arguments.get("action", "export_data"))
        observed_evidence = [str(item) for item in arguments.get("observed_evidence", [])]
        decision = policy_engine.decide(
            case_id=str(arguments.get("case_id", "")),
            action=action,
            observed_evidence=observed_evidence,
        )
        return {
            "allowed": decision.decision == "allow",
            "simulated": True,
            "policy_decision": asdict(decision),
        }

    return call
