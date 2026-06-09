# Starter Smoke Report

> Starter artifact with aggregate metrics. It checks wiring and early strategy separation.

## Overview

- Run trace: `reports/sample_run.jsonl`
- Run records: 12
- Unique cases: 3
- Overall success rate: 83.3%
- Unsupported answer rate: 16.7%
- Budget violation rate: 0.0%

## By Strategy

| group | runs | success_rate | unsupported_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|
| context_budget | 3 | 100.0% | 0.0% | 0.0% | 1.67 | 2.452 | 451.7 |
| plan_execute | 3 | 100.0% | 0.0% | 0.0% | 1.00 | 1.481 | 481.0 |
| react | 3 | 33.3% | 66.7% | 0.0% | 1.00 | 1.302 | 302.3 |
| verify_then_answer | 3 | 100.0% | 0.0% | 0.0% | 2.00 | 2.957 | 457.0 |

## By Family

| group | runs | success_rate | unsupported_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|
| retrieval_qa | 12 | 83.3% | 16.7% | 0.0% | 1.42 | 2.048 | 423.0 |

## Success-Cost View

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 33.3% | 1.302 | 302.3 | 0.0% | on current frontier |
| plan_execute | 100.0% | 1.481 | 481.0 | 0.0% | on current frontier |
| context_budget | 100.0% | 2.452 | 451.7 | 0.0% | dominated in this run |
| verify_then_answer | 100.0% | 2.957 | 457.0 | 0.0% | dominated in this run |

## Observed Strategy Splits

| case_id | family | successful_strategies | failed_strategies |
|---|---|---|---|
| cg_rag_002 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |
| cg_rag_003 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |

## Run Detail

| case_id | family | strategy | success | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---|---|---:|---|---:|---:|---:|---:|---|
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

## Failure Highlights

| case_id | strategy | failure_mode | reason |
|---|---|---|---|
| cg_rag_002 | react | unsupported_answer | missing required gold documents or budget exceeded |
| cg_rag_003 | react | unsupported_answer | missing required gold documents or budget exceeded |
