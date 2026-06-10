# Context Budget Frontier

> Seed-suite success-cost view for deterministic MVP strategies.

## Overview

- Source run trace: `reports/agent_strategy_ablation.jsonl`
- Run records: 40
- Core aggregate records: 36
- Excluded coding fixture records: 4
- Unique cases: 9
- Strategies: 4
- Overall success rate: 72.2%

## Success-Cost Table

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 44.4% | 1.127 | 293.3 | 0.0% | on current seed frontier |
| plan_execute | 66.7% | 1.292 | 458.9 | 11.1% | on current seed frontier |
| context_budget | 88.9% | 1.736 | 347.0 | 0.0% | on current seed frontier |
| verify_then_answer | 88.9% | 2.127 | 405.0 | 11.1% | dominated in this seed run |

## Pareto Notes

- Dominated strategies in this seed run: verify_then_answer.
- Dominance uses success rate and mean cost only; context and budget violations remain visible diagnostics.

## Context Budget Focus

- Split wins for `context_budget`: `cg_budget_001`, `cg_rag_002`, `cg_rag_003`, `cg_tool_001`, `cg_verify_001`
- Split losses for `context_budget`: `cg_adv_001`
- Same-outcome cases for `context_budget`: `cg_rag_001`, `cg_sensitive_001`, `cg_sensitive_002`
- Current value: the budget strategy can preserve success where another strategy fails under cost or evidence constraints.
- Current limitation: the budget strategy can still miss evidence when its conservative retrieval choice is too shallow.

## Next Policy Upgrade

The next algorithm-signal milestone is an explicit Value-of-Information policy:

```text
chunk_value = query_relevance * source_reliability * novelty
chunk_cost = estimated_context_chars + tool_cost
selection_score = chunk_value / max(chunk_cost, 1)
```

This frontier report should remain the comparison surface after the policy upgrade.
