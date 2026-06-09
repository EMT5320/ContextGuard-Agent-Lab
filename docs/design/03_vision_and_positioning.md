# Vision and Positioning

## 0. 背景快照

当前脱敏背景、作品组合和目标岗位梯度见 `08_background_snapshot.md`。与 Loomstead 的重合审计和 pivot 决策见 `09_loomstead_overlap_and_pivot.md`。

## 1. 目标画像

ContextGuard Agent Lab 面向三类岗位信号：

| 目标画像 | 项目证明方式 |
|---|---|
| Agent 算法 / 应用策略算法 | strategy ablation、context budget、verification tradeoff、success-cost frontier。 |
| Agent eval / Context Engineering | unified CaseSpec、bad-case taxonomy、adversarial context、independent grader。 |
| Agent 工程 / 大模型应用 | MCP-compatible ToolSpec、ToolExecutor、CLI、JSONL trace、Markdown report。 |

## 2. 与已有作品分工

| 资产 | 已覆盖 | ContextGuard 需要补的部分 |
|---|---|---|
| 公司项目 | 多 Agent 研判、大模型护栏、RAG 知识库、生产经验 | 公开 artifact、可复现 strategy benchmark。 |
| AlgoCoach-Flywheel | 后训练、verifier、simulator、data flywheel、eval infra | 通用 Agent 策略控制和工具协议边界。 |
| Loomstead | Agent runtime observability、trace、counterfactual replay、audit failure-analysis | 标准化 AgentStrategy ablation、MCP-compatible tool boundary、context budget frontier。 |

## 3. 项目主张

```text
MCP-compatible Agent Strategy Benchmark.
```

更具体地说，本项目要证明：

1. 主人能设计一个策略可插拔的最小 Agent benchmark。
2. 同一批任务下，不同 Agent 控制策略的成功率、工具成本和上下文成本可以被比较。
3. Verification、reflection 和 context budget 不是口号，而是可度量的 tradeoff。
4. MCP-compatible tool boundary 可以作为策略评测的结构化执行边界。

## 3.1 Round2 Final Trajectory

Round2 讨论后，项目愿景按三层推进：

| Layer | Vision | Scope Decision |
|---|---|---|
| A | Agent Strategy Benchmark | MVP：deterministic strategies + independent grader + ablation report。 |
| B | Cost-Aware Agent Control Policy | Core upgrade：VoI-based `context_budget_agent` + success-cost frontier。 |
| C | MCP-Governed Agent Evaluation | Long-term：small MCP boundary attack cases, optional identity / structured error / LLM planner work。 |

ContextGuard 的算法信号优先来自 B：把 tool use / retrieval / verification 看成预算约束下的控制策略，而不是只比较 if-else 分支。

## 4. 非目标

- 不做完整 RAG 产品平台。
- 不做 Loomstead-style Agent Behavior Observatory。
- 不做完整 Codex / Claude Code 替代品。
- 不做通用 guardrail SDK。
- 不做重 UI。
- 不承诺企业级安全效果。

## 5. 设计审稿期开放问题

1. 当前主轴是否足够支撑 Agent 算法 / 应用策略岗位？
2. `context_budget_agent` 应做到多复杂，才算有策略信号且不陷入 scope trap？
3. MCP adapter 应在 Full target 中早于 LLM-backed planner 还是反过来？
4. coding fixture 是否仍值得作为 stretch，还是完全交给 Loomstead 的 secondary coding evidence？
5. Phase 4 是否接入 cheap LLM-backed planner，取决于 eval validity 还是面试展示需要？
