"""Compare deterministic plan_execute against cheap llm_planner on rag cases."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from contextguard_agent_lab.agents.kernel import AgentKernel
from contextguard_agent_lab.benchmark.loader import load_cases
from contextguard_agent_lab.eval.metrics import summarize
from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine
from contextguard_agent_lab.tools.factory import build_default_tool_executor
from contextguard_agent_lab.trace.jsonl import write_run_records


def build_kernel(repo_root: Path) -> AgentKernel:
    """Build the benchmark kernel used by planner comparison."""

    policy = EvidencePolicyEngine.from_json(repo_root / "config" / "policies.json")
    return AgentKernel(tools=build_default_tool_executor(repo_root, policy_engine=policy), policy_engine=policy)


def _pct(value: float) -> str:
    """Format a ratio as a percentage string."""

    return f"{value * 100:.1f}%"


def build_report(records: list[dict], run_path: str) -> str:
    """Build a compact markdown comparison report."""

    by_strategy: dict[str, list[dict]] = {}
    for record in records:
        by_strategy.setdefault(str(record["strategy"]), []).append(record)

    lines = [
        "# Planner Comparison Report",
        "",
        "> Offline cheap keyword planner (`llm_planner`) vs deterministic `plan_execute` on rag_qa cases.",
        "",
        f"- Run trace: `{run_path}`",
        f"- Cases compared: {len({record['case_id'] for record in records})}",
        "",
        "| strategy | runs | success_rate | missing_verification_rate | abstain_rate | mean_tool_calls | mean_cost |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for strategy in ("plan_execute", "llm_planner"):
        metrics = summarize(by_strategy.get(strategy, []))
        lines.append(
            "| "
            f"{strategy} | "
            f"{int(metrics['case_count'])} | "
            f"{_pct(metrics['task_success_rate'])} | "
            f"{_pct(metrics['missing_verification_rate'])} | "
            f"{_pct(metrics['abstain_rate'])} | "
            f"{metrics['mean_tool_calls']:.2f} | "
            f"{metrics['mean_cost_proxy']:.3f} |"
        )

    plan_metrics = summarize(by_strategy.get("plan_execute", []))
    llm_metrics = summarize(by_strategy.get("llm_planner", []))
    delta_success = llm_metrics["task_success_rate"] - plan_metrics["task_success_rate"]
    delta_cost = llm_metrics["mean_cost_proxy"] - plan_metrics["mean_cost_proxy"]
    lines.extend(
        [
            "",
            "## Headline",
            "",
            (
                f"- `plan_execute` success: {_pct(plan_metrics['task_success_rate'])}; "
                f"`llm_planner` success: {_pct(llm_metrics['task_success_rate'])} "
                f"(delta {delta_success * 100:+.1f} pp)."
            ),
            (
                f"- Mean cost proxy: plan_execute {plan_metrics['mean_cost_proxy']:.3f}, "
                f"llm_planner {llm_metrics['mean_cost_proxy']:.3f} "
                f"(delta {delta_cost:+.3f})."
            ),
            "- Default planner backend is offline keyword policy (`data/planner/cheap_planner_policy.json`).",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="data/benchmark/cases.sample.jsonl")
    parser.add_argument("--out-jsonl", default="reports/planner_comparison.jsonl")
    parser.add_argument("--out-md", default="reports/planner_comparison.md")
    args = parser.parse_args()

    cases = [case for case in load_cases(REPO_ROOT / args.cases) if case.case_type == "rag_qa"]
    kernel = build_kernel(REPO_ROOT)
    records = [kernel.run(case, strategy=strategy) for case in cases for strategy in ("plan_execute", "llm_planner")]

    jsonl_path = REPO_ROOT / args.out_jsonl
    write_run_records(jsonl_path, records)
    from contextguard_agent_lab.trace.jsonl import read_run_records

    raw_records = read_run_records(jsonl_path)
    report = build_report(raw_records, args.out_jsonl)
    md_path = REPO_ROOT / args.out_md
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(report, encoding="utf-8")
    print(f"wrote {len(records)} records to {args.out_jsonl}")
    print(f"wrote planner comparison report to {args.out_md}")


if __name__ == "__main__":
    main()
