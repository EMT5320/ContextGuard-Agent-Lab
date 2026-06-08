# Evaluation Plan

## 1. Case families

| Family | MVP count | Purpose |
|---|---:|---|
| RAG QA | 30-50 | 检索、引用、faithfulness。 |
| Prompt injection | 10-15 | 输入级攻击。 |
| Retrieval poisoning | 10-15 | 上下文片段携带恶意指令。 |
| Sensitive action | 20 | evidence-gated tool execution。 |
| Toy code repair | 20-30 | workspace agent 修复闭环。 |

## 2. Metrics

- `task_success_rate`
- `mean_tool_calls`
- `repair_success_rate`
- `evidence_coverage`
- `unsafe_allow_rate`
- `false_block_rate`
- `mean_latency_ms`
- `cost_proxy`

## 3. Reports

- `reports/retrieval_leaderboard.md`
- `reports/agent_strategy_ablation.md`
- `reports/guardrail_eval.md`
- `reports/case_cards.md`

## 4. Case card format

每张 case card 保留：

- user task。
- selected strategy。
- key tool calls。
- policy decision。
- final result。
- failure mode / lesson。
