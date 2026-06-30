# Planner Comparison Report

> Offline cheap keyword planner (`llm_planner`) vs deterministic `plan_execute` on rag_qa cases.

- Run trace: `reports/planner_comparison.jsonl`
- Cases compared: 11

| strategy | runs | success_rate | missing_verification_rate | abstain_rate | mean_tool_calls | mean_cost |
|---|---:|---:|---:|---:|---:|---:|
| plan_execute | 11 | 72.7% | 18.2% | 0.0% | 1.00 | 1.680 |
| llm_planner | 11 | 63.6% | 0.0% | 0.0% | 1.18 | 1.853 |

## Headline

- `plan_execute` success: 72.7%; `llm_planner` success: 63.6% (delta -9.1 pp).
- Mean cost proxy: plan_execute 1.680, llm_planner 1.853 (delta +0.173).
- Default planner backend is offline keyword policy (`data/planner/cheap_planner_policy.json`).
