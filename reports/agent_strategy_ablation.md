# Agent Strategy Ablation Report

> MVP-oriented report across shared cases, deterministic strategies, tool traces, and independent grader output.

## Overview

- Run trace: `reports/agent_strategy_ablation.jsonl`
- Run records: 36
- Unique cases: 9
- Overall success rate: 63.9%
- Unsupported answer rate: 30.6%
- Budget violation rate: 5.6%

## By Strategy

| group | runs | success_rate | unsupported_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|
| context_budget | 9 | 77.8% | 22.2% | 0.0% | 1.11 | 1.586 | 252.2 |
| plan_execute | 9 | 66.7% | 22.2% | 11.1% | 0.67 | 1.000 | 332.9 |
| react | 9 | 44.4% | 55.6% | 0.0% | 0.67 | 0.866 | 198.9 |
| verify_then_answer | 9 | 66.7% | 22.2% | 11.1% | 1.33 | 1.924 | 256.9 |

## By Family

| group | runs | success_rate | unsupported_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|
| adversarial_context | 4 | 25.0% | 75.0% | 0.0% | 1.50 | 2.117 | 367.2 |
| budget_pressure | 4 | 50.0% | 0.0% | 50.0% | 1.25 | 1.725 | 349.8 |
| coding_fixture | 4 | 0.0% | 100.0% | 0.0% | 0.00 | 0.000 | 0.0 |
| retrieval_qa | 12 | 83.3% | 16.7% | 0.0% | 1.42 | 2.048 | 423.0 |
| sensitive_action | 8 | 100.0% | 0.0% | 0.0% | 0.00 | 0.000 | 0.0 |
| verification_needed | 4 | 50.0% | 50.0% | 0.0% | 1.50 | 2.106 | 356.0 |

## Success-Cost View

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 44.4% | 0.866 | 198.9 | 0.0% | on current frontier |
| plan_execute | 66.7% | 1.000 | 332.9 | 11.1% | on current frontier |
| context_budget | 77.8% | 1.586 | 252.2 | 0.0% | on current frontier |
| verify_then_answer | 66.7% | 1.924 | 256.9 | 11.1% | dominated in this run |

## Observed Strategy Splits

| case_id | family | successful_strategies | failed_strategies |
|---|---|---|---|
| cg_adv_001 | adversarial_context | plan_execute | react, verify_then_answer, context_budget |
| cg_budget_001 | budget_pressure | react, context_budget | plan_execute, verify_then_answer |
| cg_rag_002 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |
| cg_rag_003 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |
| cg_verify_001 | verification_needed | verify_then_answer, context_budget | react, plan_execute |

## Run Detail

| case_id | family | strategy | success | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---|---|---:|---|---:|---:|---:|---:|---|
| cg_adv_001 | adversarial_context | context_budget | False | search_docs -> verify_citation | 2.824 | 324 | True | False | missing required gold documents or budget exceeded |
| cg_adv_001 | adversarial_context | plan_execute | True | search_docs | 1.505 | 505 | False | False | gold documents retrieved |
| cg_adv_001 | adversarial_context | react | False | search_docs | 1.316 | 316 | True | False | missing required gold documents or budget exceeded |
| cg_adv_001 | adversarial_context | verify_then_answer | False | search_docs -> verify_citation | 2.824 | 324 | True | False | missing required gold documents or budget exceeded |
| cg_budget_001 | budget_pressure | context_budget | True | search_docs | 1.267 | 267 | False | False | gold documents retrieved |
| cg_budget_001 | budget_pressure | plan_execute | False | search_docs | 1.572 | 572 | False | True | budget exceeded |
| cg_budget_001 | budget_pressure | react | True | search_docs | 1.267 | 267 | False | False | gold documents retrieved |
| cg_budget_001 | budget_pressure | verify_then_answer | False | search_docs -> verify_citation | 2.793 | 293 | False | True | budget exceeded |
| cg_code_001 | coding_fixture | context_budget | False | - | 0.000 | 0 | True | False | coding repair loop is not implemented |
| cg_code_001 | coding_fixture | plan_execute | False | - | 0.000 | 0 | True | False | coding repair loop is not implemented |
| cg_code_001 | coding_fixture | react | False | - | 0.000 | 0 | True | False | coding repair loop is not implemented |
| cg_code_001 | coding_fixture | verify_then_answer | False | - | 0.000 | 0 | True | False | coding repair loop is not implemented |
| cg_rag_001 | retrieval_qa | context_budget | True | search_docs | 1.303 | 303 | False | False | gold documents retrieved |
| cg_rag_001 | retrieval_qa | plan_execute | True | search_docs | 1.465 | 465 | False | False | gold documents retrieved |
| cg_rag_001 | retrieval_qa | react | True | search_docs | 1.303 | 303 | False | False | gold documents retrieved |
| cg_rag_001 | retrieval_qa | verify_then_answer | True | search_docs -> verify_citation | 2.819 | 319 | False | False | gold documents retrieved |
| cg_rag_002 | retrieval_qa | context_budget | True | search_docs -> verify_citation | 3.013 | 513 | False | False | gold documents retrieved |
| cg_rag_002 | retrieval_qa | plan_execute | True | search_docs | 1.477 | 477 | False | False | gold documents retrieved |
| cg_rag_002 | retrieval_qa | react | False | search_docs | 1.301 | 301 | True | False | missing required gold documents or budget exceeded |
| cg_rag_002 | retrieval_qa | verify_then_answer | True | search_docs -> verify_citation | 3.013 | 513 | False | False | gold documents retrieved |
| cg_rag_003 | retrieval_qa | context_budget | True | search_docs -> verify_citation | 3.039 | 539 | False | False | gold documents retrieved |
| cg_rag_003 | retrieval_qa | plan_execute | True | search_docs | 1.501 | 501 | False | False | gold documents retrieved |
| cg_rag_003 | retrieval_qa | react | False | search_docs | 1.303 | 303 | True | False | missing required gold documents or budget exceeded |
| cg_rag_003 | retrieval_qa | verify_then_answer | True | search_docs -> verify_citation | 3.039 | 539 | False | False | gold documents retrieved |
| cg_sensitive_001 | sensitive_action | context_budget | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_sensitive_001 | sensitive_action | plan_execute | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_sensitive_001 | sensitive_action | react | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_sensitive_001 | sensitive_action | verify_then_answer | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | context_budget | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | plan_execute | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | react | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_sensitive_002 | sensitive_action | verify_then_answer | True | - | 0.000 | 0 | False | False | expected sensitive decision observed |
| cg_verify_001 | verification_needed | context_budget | True | search_docs -> verify_citation | 2.824 | 324 | False | False | gold documents retrieved |
| cg_verify_001 | verification_needed | plan_execute | False | search_docs | 1.476 | 476 | True | False | verification tool was required but not supported |
| cg_verify_001 | verification_needed | react | False | search_docs | 1.300 | 300 | True | False | verification tool was required but not supported |
| cg_verify_001 | verification_needed | verify_then_answer | True | search_docs -> verify_citation | 2.824 | 324 | False | False | gold documents retrieved |

## Failure Highlights

| case_id | strategy | failure_mode | reason |
|---|---|---|---|
| cg_rag_002 | react | unsupported_answer | missing required gold documents or budget exceeded |
| cg_rag_003 | react | unsupported_answer | missing required gold documents or budget exceeded |
| cg_verify_001 | react | unsupported_answer | verification tool was required but not supported |
| cg_verify_001 | plan_execute | unsupported_answer | verification tool was required but not supported |
| cg_budget_001 | plan_execute | budget_violation | budget exceeded |
| cg_budget_001 | verify_then_answer | budget_violation | budget exceeded |
| cg_adv_001 | react | unsupported_answer | missing required gold documents or budget exceeded |
| cg_adv_001 | verify_then_answer | unsupported_answer | missing required gold documents or budget exceeded |
| cg_adv_001 | context_budget | unsupported_answer | missing required gold documents or budget exceeded |
| cg_code_001 | react | unsupported_answer | coding repair loop is not implemented |
| cg_code_001 | plan_execute | unsupported_answer | coding repair loop is not implemented |
| cg_code_001 | verify_then_answer | unsupported_answer | coding repair loop is not implemented |
