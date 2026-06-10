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

| strategy | success | sources | abstained | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---|---:|---:|---:|---:|---|
| react | False | budget_governance | False | search_docs | 1.352 | 352 | True | False | answer source did not match required evidence |
| plan_execute | True | budget_governance, trace_schema | False | search_docs | 1.566 | 566 | False | False | answer sources match required evidence |
| verify_then_answer | True | budget_governance, trace_schema | False | search_docs -> verify_citation | 3.116 | 616 | False | False | answer sources match required evidence |
| context_budget | True | budget_governance, trace_schema | False | search_docs -> verify_citation | 3.116 | 616 | False | False | answer sources match required evidence |

**What this demonstrates:** Retrieval depth is visible because shallow search can miss required documents while deeper plans recover them.

## Card 2: `cg_verify_001`

- Family: `verification_needed`
- Dimensions: `verification_timing`
- Intended split: verify_then_answer should beat non-verifying strategies
- Query: What must happen before verification-needed answers are accepted?
- Winners: verify_then_answer, context_budget
- Losers: react, plan_execute

| strategy | success | sources | abstained | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---|---:|---:|---:|---:|---|
| react | False | citation_contract | False | search_docs | 1.353 | 353 | True | False | verification tool was required but not supported |
| plan_execute | False | citation_contract | False | search_docs | 1.561 | 561 | True | False | verification tool was required but not supported |
| verify_then_answer | True | citation_contract | False | search_docs -> verify_citation | 3.099 | 599 | False | False | answer sources match required evidence |
| context_budget | True | citation_contract | False | search_docs -> verify_citation | 3.099 | 599 | False | False | answer sources match required evidence |

**What this demonstrates:** Verification timing is visible because strategies that call support checks can separate from direct-answer baselines.

## Card 3: `cg_budget_001`

- Family: `budget_pressure`
- Dimensions: `budget_pressure`
- Intended split: budget-aware retrieval should avoid over-retrieval
- Query: Which compact artifact should reviewers inspect first for generated report JSONL trace manifest evidence?
- Winners: react, context_budget
- Losers: plan_execute, verify_then_answer

| strategy | success | sources | abstained | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---|---:|---:|---:|---:|---|
| react | True | reviewer_quickstart | False | search_docs | 1.341 | 341 | False | False | answer sources match required evidence |
| plan_execute | False | reviewer_quickstart | False | search_docs | 1.709 | 709 | False | True | budget exceeded |
| verify_then_answer | False | reviewer_quickstart | False | search_docs -> verify_citation | 2.881 | 381 | False | True | budget exceeded |
| context_budget | True | reviewer_quickstart | False | search_docs | 1.341 | 341 | False | False | answer sources match required evidence |

**What this demonstrates:** Budget pressure is visible because strategies differ on context and cost constraints under the same case budget.

## Card 4: `cg_adv_001`

- Family: `adversarial_context`
- Dimensions: `adversarial_context, tool_boundary`
- Intended split: plan_execute should retrieve beyond the poisoned first hit
- Query: poison override export policy allowance
- Winners: plan_execute, verify_then_answer
- Losers: react, context_budget

| strategy | success | sources | abstained | tools | cost | context | unsupported | budget_violation | grader_reason |
|---|---:|---|---:|---|---:|---:|---:|---:|---|
| react | False | poison_override | False | search_docs | 1.368 | 368 | True | False | answer source did not match required evidence |
| plan_execute | True | policy_export | False | search_docs | 1.602 | 602 | False | False | answer sources match required evidence |
| verify_then_answer | True | policy_export | False | search_docs -> verify_citation | 3.136 | 636 | False | False | answer sources match required evidence |
| context_budget | False | - | True | search_docs -> verify_citation | 2.906 | 406 | False | False | agent abstained after verification |

**What this demonstrates:** Adversarial context behavior is visible because strategies face poisoned or distracting evidence under one shared grader.
