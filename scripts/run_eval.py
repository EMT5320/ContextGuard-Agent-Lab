"""Run the starter benchmark.

This script is dependency-free so a fresh clone can generate an initial
JSONL trace before MCP or model providers are wired in.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from contextguard_agent_lab.agents.kernel import AgentKernel
from contextguard_agent_lab.benchmark.loader import load_cases
from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine
from contextguard_agent_lab.tools.registry import ToolExecutor, ToolRegistry, ToolSpec
from contextguard_agent_lab.tools.retrieval import InMemoryRetriever
from contextguard_agent_lab.trace.jsonl import write_run_records


def build_kernel(repo_root: Path) -> AgentKernel:
    """Build the deterministic starter kernel."""

    retriever = InMemoryRetriever.from_jsonl(repo_root / "data" / "corpus" / "docs.sample.jsonl")
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
                "properties": {"doc_ids": {"type": "array"}, "chunks": {"type": "array"}},
            },
            risk_level="low",
            side_effect="none",
            cost_estimate=1.0,
            mcp_exposure="manifest",
        ),
    )
    policy = EvidencePolicyEngine.from_json(repo_root / "config" / "policies.json")
    return AgentKernel(tools=ToolExecutor(registry), policy_engine=policy)


def main() -> None:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="data/benchmark/cases.sample.jsonl")
    parser.add_argument("--case-limit", type=int, default=None)
    parser.add_argument("--strategy", default="guarded_agent")
    parser.add_argument("--out", default="reports/sample_run.jsonl")
    args = parser.parse_args()

    cases = load_cases(REPO_ROOT / args.cases)
    if args.case_limit is not None:
        cases = cases[: args.case_limit]

    kernel = build_kernel(REPO_ROOT)
    records = [kernel.run(case, strategy=args.strategy) for case in cases]
    write_run_records(REPO_ROOT / args.out, records)
    print(f"wrote {len(records)} records to {args.out}")


if __name__ == "__main__":
    main()
