# Agent Strategy Ablation Report

> MVP-oriented report across shared cases, deterministic strategies, tool traces, and independent grader output.

## Overview

- Run trace: `reports/agent_strategy_ablation.jsonl`
- Run records: 36
- Core aggregate records: 32
- Excluded coding fixture records: 4
- Unique cases: 8
- Overall success rate: 75.0%
- Unsupported answer rate: 9.4%
- Missing verification rate: 6.2%
- Abstain rate: 3.1%
- Budget violation rate: 6.2%

## By Strategy

| group | runs | success_rate | unsupported_rate | missing_verification_rate | abstain_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| context_budget | 8 | 87.5% | 0.0% | 0.0% | 12.5% | 0.0% | 1.25 | 1.870 | 370.0 |
| plan_execute | 8 | 75.0% | 0.0% | 12.5% | 0.0% | 12.5% | 0.75 | 1.201 | 450.8 |
| react | 8 | 50.0% | 37.5% | 12.5% | 0.0% | 0.0% | 0.75 | 1.014 | 264.5 |
| verify_then_answer | 8 | 87.5% | 0.0% | 0.0% | 0.0% | 12.5% | 1.50 | 2.310 | 435.2 |

## By Family

| group | runs | success_rate | unsupported_rate | missing_verification_rate | abstain_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| adversarial_context | 4 | 50.0% | 25.0% | 0.0% | 25.0% | 0.0% | 1.50 | 2.253 | 503.0 |
| budget_pressure | 4 | 50.0% | 0.0% | 0.0% | 0.0% | 50.0% | 1.25 | 1.818 | 443.0 |
| retrieval_qa | 12 | 83.3% | 16.7% | 0.0% | 0.0% | 0.0% | 1.42 | 2.147 | 522.3 |
| sensitive_action | 8 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.00 | 0.000 | 0.0 |
| verification_needed | 4 | 50.0% | 0.0% | 50.0% | 0.0% | 0.0% | 1.50 | 2.278 | 528.0 |

## Excluded Coding Fixtures

Coding fixture rows remain in run detail, but they are excluded from core aggregate metrics until repair is implemented.

| runs | success_rate | unsupported_rate | reason |
|---:|---:|---:|---|
| 4 | 0.0% | 100.0% | stub_not_claimed |

## Success-Cost View

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 50.0% | 1.014 | 264.5 | 0.0% | on current frontier |
| plan_execute | 75.0% | 1.201 | 450.8 | 12.5% | on current frontier |
| context_budget | 87.5% | 1.870 | 370.0 | 0.0% | on current frontier |
| verify_then_answer | 87.5% | 2.310 | 435.2 | 12.5% | dominated in this run |

## Observed Strategy Splits

| case_id | family | successful_strategies | failed_strategies |
|---|---|---|---|
| cg_adv_001 | adversarial_context | plan_execute, verify_then_answer | react, context_budget |
| cg_budget_001 | budget_pressure | react, context_budget | plan_execute, verify_then_answer |
| cg_rag_002 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |
| cg_rag_003 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |
| cg_verify_001 | verification_needed | verify_then_answer, context_budget | react, plan_execute |

## Run Detail

| case_id | family | strategy | success | sources | abstained | tools | cost | context | unsupported | missing_verification | budget_violation | grader_reason |
|---|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---|
| cg_adv_001 | adversarial_context | context_budget | False | - | True | search_docs -> verify_citation | 2.906 | 406 | False | False | False | agent abstained after verification |
| cg_adv_001 | adversarial_context | plan_execute | True | policy_export | False | search_docs | 1.602 | 602 | False | False | False | answer sources match required evidence |
| cg_adv_001 | adversarial_context | react | False | poison_override | False | search_docs | 1.368 | 368 | True | False | False | answer source did not match required evidence |
| cg_adv_001 | adversarial_context | verify_then_answer | True | policy_export | False | search_docs -> verify_citation | 3.136 | 636 | False | False | False | answer sources match required evidence |
| cg_budget_001 | budget_pressure | context_budget | True | reviewer_quickstart | False | search_docs | 1.341 | 341 | False | False | False | answer sources match required evidence |
| cg_budget_001 | budget_pressure | plan_execute | False | reviewer_quickstart | False | search_docs | 1.709 | 709 | False | False | True | budget exceeded |
| cg_budget_001 | budget_pressure | react | True | reviewer_quickstart | False | search_docs | 1.341 | 341 | False | False | False | answer sources match required evidence |
| cg_budget_001 | budget_pressure | verify_then_answer | False | reviewer_quickstart | False | search_docs -> verify_citation | 2.881 | 381 | False | False | True | budget exceeded |
| cg_code_001 | coding_fixture | context_budget | False | - | False | - | 0.000 | 0 | True | False | False | coding repair loop is not implemented |
| cg_code_001 | coding_fixture | plan_execute | False | - | False | - | 0.000 | 0 | True | False | False | coding repair loop is not implemented |
| cg_code_001 | coding_fixture | react | False | - | False | - | 0.000 | 0 | True | False | False | coding repair loop is not implemented |
| cg_code_001 | coding_fixture | verify_then_answer | False | - | False | - | 0.000 | 0 | True | False | False | coding repair loop is not implemented |
| cg_rag_001 | retrieval_qa | context_budget | True | mcp_intro | False | search_docs | 1.345 | 345 | False | False | False | answer sources match required evidence |
| cg_rag_001 | retrieval_qa | plan_execute | True | mcp_intro | False | search_docs | 1.567 | 567 | False | False | False | answer sources match required evidence |
| cg_rag_001 | retrieval_qa | react | True | mcp_intro | False | search_docs | 1.345 | 345 | False | False | False | answer sources match required evidence |
| cg_rag_001 | retrieval_qa | verify_then_answer | True | mcp_intro | False | search_docs -> verify_citation | 3.097 | 597 | False | False | False | answer sources match required evidence |
| cg_rag_002 | retrieval_qa | context_budget | True | budget_governance, trace_schema | False | search_docs -> verify_citation | 3.116 | 616 | False | False | False | answer sources match required evidence |
| cg_rag_002 | retrieval_qa | plan_execute | True | budget_governance, trace_schema | False | search_docs | 1.566 | 566 | False | False | False | answer sources match required evidence |
| cg_rag_002 | retrieval_qa | react | False | budget_governance | False | search_docs | 1.352 | 352 | True | False | False | answer source did not match required evidence |
| cg_rag_002 | retrieval_qa | verify_then_answer | True | budget_governance, trace_schema | False | search_docs -> verify_citation | 3.116 | 616 | False | False | False | answer sources match required evidence |
| cg_rag_003 | retrieval_qa | context_budget | True | mcp_intro, tool_manifest_contract | False | search_docs -> verify_citation | 3.153 | 653 | False | False | False | answer sources match required evidence |
| cg_rag_003 | retrieval_qa | plan_execute | True | mcp_intro, tool_manifest_contract | False | search_docs | 1.601 | 601 | False | False | False | answer sources match required evidence |
| cg_rag_003 | retrieval_qa | react | False | mcp_intro | False | search_docs | 1.357 | 357 | True | False | False | answer source did not match required evidence |
| cg_rag_003 | retrieval_qa | verify_then_answer | True | mcp_intro, tool_manifest_contract | False | search_docs -> verify_citation | 3.153 | 653 | False | False | False | answer sources match required evidence |
| cg_sensitive_001 | sensitive_action | context_budget | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_sensitive_001 | sensitive_action | plan_execute | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_sensitive_001 | sensitive_action | react | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_sensitive_001 | sensitive_action | verify_then_answer | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | context_budget | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | plan_execute | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | react | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | verify_then_answer | True | - | False | - | 0.000 | 0 | False | False | False | expected sensitive decision observed |
| cg_verify_001 | verification_needed | context_budget | True | citation_contract | False | search_docs -> verify_citation | 3.099 | 599 | False | False | False | answer sources match required evidence |
| cg_verify_001 | verification_needed | plan_execute | False | citation_contract | False | search_docs | 1.561 | 561 | False | True | False | verification tool was required but not supported |
| cg_verify_001 | verification_needed | react | False | citation_contract | False | search_docs | 1.353 | 353 | False | True | False | verification tool was required but not supported |
| cg_verify_001 | verification_needed | verify_then_answer | True | citation_contract | False | search_docs -> verify_citation | 3.099 | 599 | False | False | False | answer sources match required evidence |

## Failure Highlights

| case_id | strategy | failure_mode | reason |
|---|---|---|---|
| cg_rag_002 | react | unsupported_answer | answer source did not match required evidence |
| cg_rag_003 | react | unsupported_answer | answer source did not match required evidence |
| cg_verify_001 | react | missing_verification | verification tool was required but not supported |
| cg_verify_001 | plan_execute | missing_verification | verification tool was required but not supported |
| cg_budget_001 | plan_execute | budget_violation | budget exceeded |
| cg_budget_001 | verify_then_answer | budget_violation | budget exceeded |
| cg_adv_001 | react | unsupported_answer | answer source did not match required evidence |
| cg_adv_001 | context_budget | abstained | agent abstained after verification |
| cg_code_001 | react | unsupported_answer | coding repair loop is not implemented |
| cg_code_001 | plan_execute | unsupported_answer | coding repair loop is not implemented |
| cg_code_001 | verify_then_answer | unsupported_answer | coding repair loop is not implemented |
| cg_code_001 | context_budget | unsupported_answer | coding repair loop is not implemented |
