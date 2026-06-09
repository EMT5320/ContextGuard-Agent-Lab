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

## 1.1 Case Design Dimensions

Case authoring must start from strategy-difference dimensions. A case can belong to a task family, but it should also declare which strategy behavior it is meant to separate.

| Dimension | Case Design Principle | Expected Strategy Split |
|---|---|---|
| Retrieval depth | Gold evidence requires 2+ retrieval/read steps | `plan_execute` beats `react`。 |
| Verification timing | Plausible answer is unsupported without citation check | `verify_then_answer` beats `react`。 |
| Budget pressure | Context window cannot include all retrieved chunks | `context_budget` saves cost but may miss evidence。 |
| Adversarial context | Poisoned/distractor doc conflicts with reliable evidence | Verification and budget policies resist distractor better。 |
| Tool boundary | Distractor tries to trigger an inappropriate tool | Tool-aware strategies avoid wrong / unsafe tool calls。 |

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
- `success_conditioned_cost`
- `pareto_dominated_case_count`

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

## 3.1 Cost Proxy and Frontier

The first cost formula can be simple, but it must be explicit:

```text
cost_proxy = tool_calls + verification_calls * 1.5 + context_chars_used / 1000
```

Reports should include raw success rate, success-conditioned cost, budget violation rate, and a Pareto-style frontier. A strategy is dominated on a case when another strategy succeeds with equal or lower cost and at least one strictly better metric.

## 4. Report Contract

主报告必须包含：

- Overall summary。
- By strategy leaderboard。
- By family metrics。
- Success-cost frontier。
- Pareto / dominated strategy notes。
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
- `context_budget_agent` 必须解释 value-of-information heuristic 的成功和失败，不只输出低成本数字。
- 报告要解释差异原因，不只输出 leaderboard。
