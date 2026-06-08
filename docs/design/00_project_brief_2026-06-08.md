# ContextGuard Agent Lab 项目简报（2026-06-08）

## 1. 一句话定位

ContextGuard Agent Lab 是一个 MCP-native、evidence-governed 的 Agent 评测工作台，用统一 benchmark 评估 Agent 在上下文获取、工具执行、敏感动作拦截、失败修复和可追溯性上的表现。

## 2. 当前画像与开工动机

现有求职资产已经覆盖：

- 公司项目：多 Agent 研判、大模型护栏、RAG 知识库、安全微服务、文件综合研判。
- AlgoCoach-Flywheel：后训练、verifier、simulator、data flywheel、eval infrastructure。
- Loomstead：Agent runtime observability、trace、counterfactual replay、audit case cards。

剩余需要公开补强的能力：

- 标准协议边界：MCP / optional A2A。
- 可评测 Agent kernel：plan / act / observe / reflect / repair。
- RAG + Agent 融合策略：检索收益、成本、上下文预算。
- Evidence-gated tool execution：敏感工具调用的证据契约与审计。
- Coding-agent-like workspace loop：读取失败、修改、重跑、记录 trace。

## 3. 推荐项目主张

原始 ContextGuard Lab 偏向 RAG / Guardrail workbench。为冲 Agent 算法、应用策略算法、Agent 评测算法岗位，本项目主轴升级为：

```text
Agent kernel + MCP tools + evidence policy + eval harness + case cards
```

## 4. 一个月成功定义

```text
[ ] 80-120 条总 case。
[ ] 20+ toy code repair tasks。
[ ] MCP retrieval + workspace tools 跑通。
[ ] 至少 4 种 agent strategy 对比。
[ ] guarded agent 产出 evidence gate trace。
[ ] full report 包含 success / safety / cost / latency / ablation。
[ ] 3 张 case card：RAG、guardrail、code repair。
```

## 5. 坍缩防线

- 不做通用 RAG 产品平台。
- 不做重 UI。
- 不堆普通 guardrail 样例。
- A2A 只作为 W4 thin reviewer handoff。
- 所有功能必须进入 metric、trace、report 或 case card。
- 不引入公司数据和内部策略。
