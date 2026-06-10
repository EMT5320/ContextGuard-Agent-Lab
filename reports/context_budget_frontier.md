# Context Budget Frontier

> Seed-suite success-cost view for deterministic MVP strategies.

## Overview

- Source run trace: `reports/agent_strategy_ablation.jsonl`
- Run records: 36
- Unique cases: 9
- Strategies: 4
- Overall success rate: 66.7%

## Success-Cost Table

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 44.4% | 0.902 | 235.1 | 0.0% | on current seed frontier |
| plan_execute | 66.7% | 1.067 | 400.7 | 11.1% | on current seed frontier |
| context_budget | 77.8% | 1.662 | 328.9 | 0.0% | on current seed frontier |
| verify_then_answer | 77.8% | 2.054 | 386.9 | 11.1% | dominated in this seed run |

## Pareto Notes

- Dominated strategies in this seed run: verify_then_answer.
- Dominance uses success rate and mean cost only; context and budget violations remain visible diagnostics.

## Context Budget Focus

- Split wins for `context_budget`: `cg_budget_001`, `cg_rag_002`, `cg_rag_003`, `cg_verify_001`
- Split losses for `context_budget`: `cg_adv_001`
- Same-outcome cases for `context_budget`: `cg_code_001`, `cg_rag_001`, `cg_sensitive_001`, `cg_sensitive_002`
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
