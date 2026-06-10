# Starter Smoke Report

> Starter artifact with aggregate metrics. It checks wiring and early strategy separation.

## Overview

- Run trace: `reports/sample_run.jsonl`
- Run records: 12
- Core aggregate records: 12
- Excluded coding fixture records: 0
- Unique cases: 3
- Overall success rate: 83.3%
- Unsupported answer rate: 16.7%
- Missing verification rate: 0.0%
- Abstain rate: 0.0%
- Wrong tool call rate: 0.0%
- Budget violation rate: 0.0%

## By Strategy

| group | runs | success_rate | unsupported_rate | missing_verification_rate | abstain_rate | wrong_tool_call_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| context_budget | 3 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.67 | 2.538 | 538.0 |
| plan_execute | 3 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.00 | 1.578 | 578.0 |
| react | 3 | 33.3% | 66.7% | 0.0% | 0.0% | 0.0% | 0.0% | 1.00 | 1.351 | 351.3 |
| verify_then_answer | 3 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.00 | 3.122 | 622.0 |

## By Family

| group | runs | success_rate | unsupported_rate | missing_verification_rate | abstain_rate | wrong_tool_call_rate | budget_violation_rate | mean_tool_calls | mean_cost | mean_context |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| retrieval_qa | 12 | 83.3% | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | 1.42 | 2.147 | 522.3 |

## Success-Cost View

| strategy | success_rate | mean_cost | mean_context | budget_violation_rate | frontier_note |
|---|---:|---:|---:|---:|---|
| react | 33.3% | 1.351 | 351.3 | 0.0% | on current frontier |
| plan_execute | 100.0% | 1.578 | 578.0 | 0.0% | on current frontier |
| context_budget | 100.0% | 2.538 | 538.0 | 0.0% | dominated in this run |
| verify_then_answer | 100.0% | 3.122 | 622.0 | 0.0% | dominated in this run |

## Observed Strategy Splits

| case_id | family | successful_strategies | failed_strategies |
|---|---|---|---|
| cg_rag_002 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |
| cg_rag_003 | retrieval_qa | plan_execute, verify_then_answer, context_budget | react |

## Run Detail

| case_id | family | strategy | success | sources | abstained | tools | cost | context | unsupported | missing_verification | wrong_tool_call | budget_violation | grader_reason |
|---|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| cg_rag_001 | retrieval_qa | context_budget | True | mcp_intro | False | search_docs | 1.345 | 345 | False | False | False | False | answer sources match required evidence |
| cg_rag_001 | retrieval_qa | plan_execute | True | mcp_intro | False | search_docs | 1.567 | 567 | False | False | False | False | answer sources match required evidence |
| cg_rag_001 | retrieval_qa | react | True | mcp_intro | False | search_docs | 1.345 | 345 | False | False | False | False | answer sources match required evidence |
| cg_rag_001 | retrieval_qa | verify_then_answer | True | mcp_intro | False | search_docs -> verify_citation | 3.097 | 597 | False | False | False | False | answer sources match required evidence |
| cg_rag_002 | retrieval_qa | context_budget | True | budget_governance, trace_schema | False | search_docs -> verify_citation | 3.116 | 616 | False | False | False | False | answer sources match required evidence |
| cg_rag_002 | retrieval_qa | plan_execute | True | budget_governance, trace_schema | False | search_docs | 1.566 | 566 | False | False | False | False | answer sources match required evidence |
| cg_rag_002 | retrieval_qa | react | False | budget_governance | False | search_docs | 1.352 | 352 | True | False | False | False | answer source did not match required evidence |
| cg_rag_002 | retrieval_qa | verify_then_answer | True | budget_governance, trace_schema | False | search_docs -> verify_citation | 3.116 | 616 | False | False | False | False | answer sources match required evidence |
| cg_rag_003 | retrieval_qa | context_budget | True | mcp_intro, tool_manifest_contract | False | search_docs -> verify_citation | 3.153 | 653 | False | False | False | False | answer sources match required evidence |
| cg_rag_003 | retrieval_qa | plan_execute | True | mcp_intro, tool_manifest_contract | False | search_docs | 1.601 | 601 | False | False | False | False | answer sources match required evidence |
| cg_rag_003 | retrieval_qa | react | False | mcp_intro | False | search_docs | 1.357 | 357 | True | False | False | False | answer source did not match required evidence |
| cg_rag_003 | retrieval_qa | verify_then_answer | True | mcp_intro, tool_manifest_contract | False | search_docs -> verify_citation | 3.153 | 653 | False | False | False | False | answer sources match required evidence |

## Failure Highlights

| case_id | strategy | failure_mode | reason |
|---|---|---|---|
| cg_rag_002 | react | unsupported_answer | answer source did not match required evidence |
| cg_rag_003 | react | unsupported_answer | answer source did not match required evidence |
