# Representative Case Cards

> Seed-suite examples that make current strategy differences inspectable.

## Overview

- Source run trace: `reports/agent_strategy_ablation.jsonl`
- Cards rendered: 4
- Selection: split cases first, then high-value dimensions in stable order.

## Card 1: `cg_rag_002`

- Family: `retrieval_qa`
- Dimensions: `retrieval_depth`
- Intended split: plan_execute and verify_then_answer should beat react
- Query: Which budget governance and trace schema records make strategy comparison auditable?
- Winners: plan_execute, verify_then_answer, context_budget
- Losers: react

| strategy | success | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---:|---:|---:|---|
| react | False | search_docs | 1.301 | 301 | True | False | missing required gold documents or budget exceeded |
| plan_execute | True | search_docs | 1.477 | 477 | False | False | gold documents retrieved |
| verify_then_answer | True | search_docs -> verify_citation | 3.013 | 513 | False | False | gold documents retrieved |
| context_budget | True | search_docs -> verify_citation | 3.013 | 513 | False | False | gold documents retrieved |

**What this demonstrates:** Retrieval depth is visible because shallow search can miss required documents while deeper plans recover them.

## Card 2: `cg_verify_001`

- Family: `verification_needed`
- Dimensions: `verification_timing`
- Intended split: verify_then_answer should beat non-verifying strategies
- Query: What must happen before verification-needed answers are accepted?
- Winners: verify_then_answer, context_budget
- Losers: react, plan_execute

| strategy | success | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---:|---:|---:|---|
| react | False | search_docs | 1.300 | 300 | True | False | verification tool was required but not supported |
| plan_execute | False | search_docs | 1.476 | 476 | True | False | verification tool was required but not supported |
| verify_then_answer | True | search_docs -> verify_citation | 2.824 | 324 | False | False | gold documents retrieved |
| context_budget | True | search_docs -> verify_citation | 2.824 | 324 | False | False | gold documents retrieved |

**What this demonstrates:** Verification timing is visible because strategies that call support checks can separate from direct-answer baselines.

## Card 3: `cg_budget_001`

- Family: `budget_pressure`
- Dimensions: `budget_pressure`
- Intended split: budget-aware retrieval should avoid over-retrieval
- Query: Which compact artifact should reviewers inspect first for generated report JSONL trace manifest evidence?
- Winners: react, context_budget
- Losers: plan_execute, verify_then_answer

| strategy | success | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---:|---:|---:|---|
| react | True | search_docs | 1.267 | 267 | False | False | gold documents retrieved |
| plan_execute | False | search_docs | 1.572 | 572 | False | True | budget exceeded |
| verify_then_answer | False | search_docs -> verify_citation | 2.793 | 293 | False | True | budget exceeded |
| context_budget | True | search_docs | 1.267 | 267 | False | False | gold documents retrieved |

**What this demonstrates:** Budget pressure is visible because strategies differ on context and cost constraints under the same case budget.

## Card 4: `cg_adv_001`

- Family: `adversarial_context`
- Dimensions: `adversarial_context, tool_boundary`
- Intended split: plan_execute should retrieve beyond the poisoned first hit
- Query: poison override export policy allowance
- Winners: plan_execute
- Losers: react, verify_then_answer, context_budget

| strategy | success | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---:|---:|---:|---|
| react | False | search_docs | 1.316 | 316 | True | False | missing required gold documents or budget exceeded |
| plan_execute | True | search_docs | 1.505 | 505 | False | False | gold documents retrieved |
| verify_then_answer | False | search_docs -> verify_citation | 2.824 | 324 | True | False | missing required gold documents or budget exceeded |
| context_budget | False | search_docs -> verify_citation | 2.824 | 324 | True | False | missing required gold documents or budget exceeded |

**What this demonstrates:** Adversarial context behavior is visible because strategies face poisoned or distracting evidence under one shared grader.
