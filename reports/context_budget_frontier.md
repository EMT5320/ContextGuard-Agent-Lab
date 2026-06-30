# Context Budget Frontier

> Seed-suite success-cost view for deterministic MVP strategies.

## Overview

- Source run trace: `reports/agent_strategy_ablation.jsonl`
- Run records: 68
- Core aggregate records: 64
- Excluded coding fixture records: 4
- Unique cases: 16
- Strategies: 4
- Overall success rate: 71.9%

## Success-Cost Table

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 31.2% | 1.174 | 330.7 | 0.0% | on current seed frontier |
| plan_execute | 68.8% | 1.368 | 524.7 | 6.2% | on current seed frontier |
| context_budget | 93.8% | 2.013 | 450.9 | 0.0% | on current seed frontier |
| verify_then_answer | 93.8% | 2.234 | 483.5 | 6.2% | dominated in this seed run |

## Pareto Notes

- Dominated strategies in this seed run: verify_then_answer.
- Dominance uses success rate and mean cost only; context and budget violations remain visible diagnostics.

## Context Budget Focus

- Split wins for `context_budget`: `cg_budget_001`, `cg_rag_002`, `cg_rag_003`, `cg_sec_cve_001`, `cg_sec_ioc_export_001`, `cg_sec_prompt_001`, `cg_sec_report_verify_001`, `cg_sec_source_001`, `cg_tool_001`, `cg_trust_001`, `cg_verify_001`
- Split losses for `context_budget`: `cg_adv_001`
- Same-outcome cases for `context_budget`: `cg_rag_001`, `cg_sec_export_001`, `cg_sensitive_001`, `cg_sensitive_002`
- Current value: the budget strategy can preserve success where another strategy fails under cost or evidence constraints.
- Current limitation: the budget strategy can still miss evidence when its conservative retrieval choice is too shallow.

## Selection Trace Samples

- `cg_sec_cve_001` selected `sec_official_advisory`; skipped `sec_forged_cve_post` (lower_source_reliability).
- `cg_sec_prompt_001` selected `sec_prompt_injection_policy`; skipped `sec_prompt_injection_note` (lower_source_reliability).
- `cg_sec_report_verify_001` selected `sec_triage_report_standard`; skipped `sec_pastebin_key_rumor` (lower_source_reliability).
- `cg_sec_source_001` selected `sec_incident_runbook`; skipped `sec_pastebin_key_rumor` (lower_source_reliability).
- `cg_trust_001` selected `release_gate_policy`; skipped `release_gate_blog` (lower_source_reliability).

## Value Heuristic

The current `context_budget` skeleton records a label-free greedy value signal:

```text
chunk_value = query_relevance * source_reliability * novelty
chunk_cost = estimated_context_chars
selection_score = chunk_value / max(chunk_cost, 1)
```

Selection reasons are emitted under `record.metrics.selection_reasons`; the next upgrade is to tune this heuristic against larger case coverage.
