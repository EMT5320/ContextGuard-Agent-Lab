# Evaluation Plan

## 1. Case Families

MVP 追求 20-30 条高质量 case，Full target 再扩到 60-80 条。数量不替代有效性；每个 family 都需要正例、失败例和可解释 bad case。

| Family | MVP Count | Full Count | Purpose |
|---|---:|---:|---|
| Retrieval QA | 6-8 | 15-20 | 检索、引用、answer support。 |
| Adversarial Context | 5-6 | 10-15 | prompt injection / poisoned snippet / distractor doc。 |
| Verification Needed | 5-6 | 10-15 | 验证前回答容易 unsupported，验证后可修正。 |
| Budget Pressure | 5-6 | 10-15 | context_budget 与 plan_execute 的 success-cost tradeoff。 |
| Tool Selection | 3-5 | 8-10 | 同一任务下不同工具选择成本不同。 |
| Sensitive Action | 2-3 | 5-8 | 小规模 allow / block / review 平衡集。 |
| Coding Fixture | 0-2 | 5-8 | stretch，仅做 bounded repair / test cases。 |

## 2. Metrics

### Required Metrics

- `task_success_rate`
- `mean_tool_calls`
- `cost_proxy`
- `context_chars_used`
- `budget_violation_rate`
- `citation_coverage`
- `unsupported_answer_rate`
- `verification_call_rate`
- `reflection_recovery_rate`

### Conditional Metrics

- `unsafe_allow_rate`：仅 sensitive action family。
- `false_block_rate`：仅 sensitive action family。
- `repair_success_rate`：仅 coding fixture family。
- `mean_latency_ms`：ToolExecutor 真实计时后启用。

## 3. Reports

- `reports/agent_strategy_ablation.md`
- `reports/context_budget_frontier.md`
- `reports/adversarial_context_eval.md`
- `reports/failure_taxonomy.md`
- `reports/case_cards.md`

## 4. Report Contract

主报告必须包含：

- Overall summary。
- By strategy leaderboard。
- By family metrics。
- Success-cost frontier。
- Bad-case taxonomy。
- Top 3 case cards。
- Claim evidence table。

## 5. Case Card Format

每张 case card 保留：

- user task。
- selected strategy。
- budget constraints。
- important tool calls。
- verification / grader result。
- final result。
- why another strategy failed or spent more。
- honest limitation。

## 6. Eval Validity Rules

- Success 判定必须由 independent grader 执行，不放在 AgentKernel 分支里。
- 至少 20-30% cases 应让某些策略失败或超预算。
- Adversarial context 必须有 negative control。
- Budget case 必须展示 success-cost tradeoff，而不是只展示省钱。
- 报告要解释差异原因，不只输出 leaderboard。
