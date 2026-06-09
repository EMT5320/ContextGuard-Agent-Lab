# Decision: Initial Scope Revised

- 背景：求职冲刺期需要公开展示 Agent 系统与 Agent Eval 能力，并补齐更高级 Agent 算法 / 应用策略岗位的公开证据。
- 原选项 A：普通 MCP RAG / Guardrail workbench；ROI 稳定但算法岗信号偏弱。
- 原选项 B：完整 coding agent；展示强但工期和风险过高。
- 原选项 C：Agent kernel + MCP tools + eval harness；兼顾高级岗位信号和一月交付。
- 初始推荐：选项 C。
- 2026-06-09 修订原因：对 Loomstead 进行真实重合审计后发现，observability、trace、counterfactual replay、audit failure-analysis 已由 Loomstead 承担。ContextGuard 如果继续主打 evidence-gated execution，会在作品集叙事上重复。
- 当前决策：保留 ContextGuard，但从 `evidence-governed agent workbench` pivot 为 `MCP-compatible Agent Strategy Benchmark`。
- 新主轴：AgentStrategy ablation、ToolSpec / ToolExecutor、context budget、verification-before-answer、success-cost frontier。
- Cut：A2A、重 UI、通用 RAG 平台、完整 coding agent、Loomstead-style observability / audit 主线。
