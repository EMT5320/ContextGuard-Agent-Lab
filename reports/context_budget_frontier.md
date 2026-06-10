# Context Budget Frontier

> Seed-suite success-cost view for deterministic MVP strategies.

## Overview

- Source run trace: `reports/agent_strategy_ablation.jsonl`
- Run records: 44
- Core aggregate records: 40
- Excluded coding fixture records: 4
- Unique cases: 10
- Strategies: 4
- Overall success rate: 72.5%

## Success-Cost Table

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 40.0% | 1.161 | 310.8 | 0.0% | on current seed frontier |
| plan_execute | 70.0% | 1.337 | 487.0 | 10.0% | on current seed frontier |
| context_budget | 90.0% | 1.890 | 390.3 | 0.0% | on current seed frontier |
| verify_then_answer | 90.0% | 2.243 | 442.5 | 10.0% | dominated in this seed run |

## Pareto Notes

- Dominated strategies in this seed run: verify_then_answer.
- Dominance uses success rate and mean cost only; context and budget violations remain visible diagnostics.

## Context Budget Focus

- Split wins for `context_budget`: `cg_budget_001`, `cg_rag_002`, `cg_rag_003`, `cg_tool_001`, `cg_trust_001`, `cg_verify_001`
- Split losses for `context_budget`: `cg_adv_001`
- Same-outcome cases for `context_budget`: `cg_rag_001`, `cg_sensitive_001`, `cg_sensitive_002`
- Current value: the budget strategy can preserve success where another strategy fails under cost or evidence constraints.
- Current limitation: the budget strategy can still miss evidence when its conservative retrieval choice is too shallow.

## Selection Trace Samples

- `cg_trust_001` selected `release_gate_policy`; skipped `release_gate_blog` (lower_source_reliability).
- `cg_verify_001` selected `citation_contract`; skipped `budget_governance` (low_query_relevance).
- `cg_adv_001` selected `poison_override`; skipped none.
- `cg_budget_001` selected `reviewer_quickstart`; skipped none.
- `cg_rag_001` selected `mcp_intro`; skipped none.

## Value Heuristic

The current `context_budget` skeleton records a label-free greedy value signal:

```text
chunk_value = query_relevance * source_reliability * novelty
chunk_cost = estimated_context_chars
selection_score = chunk_value / max(chunk_cost, 1)
```

Selection reasons are emitted under `record.metrics.selection_reasons`; the next upgrade is to tune this heuristic against larger case coverage.
