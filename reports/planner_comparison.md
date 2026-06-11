# Planner Comparison Report

> Offline cheap keyword planner (`llm_planner`) vs deterministic `plan_execute` on rag_qa cases.

- Run trace: `reports/planner_comparison.jsonl`
- Cases compared: 7

| strategy | runs | success_rate | missing_verification_rate | abstain_rate | mean_tool_calls | mean_cost |
|---|---:|---:|---:|---:|---:|---:|
| plan_execute | 7 | 71.4% | 14.3% | 0.0% | 1.00 | 1.622 |
| llm_planner | 7 | 71.4% | 0.0% | 0.0% | 1.14 | 1.776 |

## Headline

- `plan_execute` success: 71.4%; `llm_planner` success: 71.4% (delta +0.0 pp).
- Mean cost proxy: plan_execute 1.622, llm_planner 1.776 (delta +0.155).
- Default planner backend is offline keyword policy (`data/planner/cheap_planner_policy.json`).
