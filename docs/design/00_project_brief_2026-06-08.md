# ContextGuard Agent Lab 项目简报（2026-06-08）

## 1. 一句话定位

ContextGuard Agent Lab 是一个 MCP-compatible Agent Strategy Benchmark，用统一任务集评估不同 Agent 策略在检索、工具调用、验证、反思和上下文预算上的成功率与成本权衡。

英文版：

```text
A reproducible benchmark for studying cost-aware agent control policies across retrieval, verification, reflection, and tool-use tasks.
```

## 2. 开工动机

现有求职资产已经覆盖：

- 公司项目：多 Agent 研判、大模型护栏、RAG 知识库、安全微服务、文件综合研判。
- AlgoCoach-Flywheel：后训练、verifier、simulator、data flywheel、eval infrastructure。
- Loomstead：Agent runtime observability、trace、counterfactual replay、audit failure-analysis、portfolio case cards。

剩余需要公开补强的能力：

- MCP-compatible 工具协议边界。
- 多 Agent strategy 的统一 benchmark 与 ablation。
- Context budget / tool budget / verification budget 的 success-cost frontier。
- RAG + adversarial context 的策略评测，而不是 RAG 产品平台。
- 面向 Agent 算法 / 应用策略岗位的报告化实验结论。

## 3. 推荐项目主张

旧版主轴偏 `evidence-governed tool execution`，与 Loomstead 的 audit / trace 展示重合。新版主轴收敛为：

```text
Agent strategy eval + MCP-compatible tools + context budget + verification + ablation report
```

项目要回答的问题：

1. 同一批任务下，`react`、`plan_execute`、`verify_then_answer`、`reflective`、`context_budget` 策略有什么行为差异？
2. 哪些策略更成功，哪些策略更省工具调用 / 上下文 / 验证成本？
3. 在 adversarial context 和 unsupported-answer 风险下，验证策略是否值得额外成本？
4. MCP-compatible tool boundary 如何让策略评测保持结构化、可复现、可扩展？

## 4. 一个月 Portfolio MVP 成功定义

```text
[ ] 4 个真实可区分策略：react / plan_execute / verify_then_answer / context_budget。
[ ] ToolSpec + ToolRegistry + ToolExecutor，所有工具调用结构化可追踪。
[ ] 20-30 条高质量 case，覆盖 retrieval QA、adversarial context、verification-needed、budget pressure。
[ ] strategy ablation report 展示 success / tool calls / context chars / cost_proxy / unsupported_answer_rate。
[ ] 至少 3 个 bad case 进入 failure taxonomy。
[ ] README 首页能从 claim 跳到 leaderboard、report 和代表性 case card。
```

Full target 可以再加入 FastMCP adapter、reflective repair、少量 sensitive action 与 coding fixture。

## 5. 坍缩防线

- 不做通用 RAG 产品平台。
- 不做 Loomstead 已覆盖的 observability / audit 主线。
- 不做完整 coding agent。
- 不做重 UI。
- `MCP-compatible` 在 FastMCP adapter 跑通前只声明 tool contract / in-process boundary。
- 所有功能必须进入 metric、trace、report 或 case card。
- 不引入公司数据和内部策略。
