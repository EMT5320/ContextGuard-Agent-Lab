# Vision and Positioning

## 0. 背景快照

当前脱敏背景、作品组合和目标岗位梯度见 `08_background_snapshot.md`。

## 1. 目标画像

ContextGuard Agent Lab 面向三类岗位信号：

| 目标画像 | 项目证明方式 |
|---|---|
| Agent 工程 / 大模型应用 | 可运行 Agent kernel、工具调用、trace、fallback、case report。 |
| Agent 算法 / 应用策略算法 | strategy ablation、context budget、reflection/repair、success-cost tradeoff。 |
| Agent 评测 / 安全护栏 | unified CaseSpec、policy decision、unsafe allow / false block、bad-case taxonomy。 |

## 2. 与已有作品分工

| 资产 | 已覆盖 | ContextGuard 需要补的部分 |
|---|---|---|
| 公司项目 | 多 Agent 研判、大模型护栏、RAG 知识库、生产经验 | 公开 artifact、可复现 benchmark、可展示 case cards。 |
| AlgoCoach-Flywheel | 后训练、verifier、simulator、data flywheel、eval infra | 通用 Agent kernel、MCP tool boundary、workspace task loop。 |
| Loomstead | Agent runtime observability、trace、counterfactual replay | 标准协议边界、策略 ablation、求职可读技术报告。 |

## 3. 项目主张

```text
MCP-native, evidence-governed agent evaluation workbench.
```

更具体地说，本项目要证明：

1. 浮浮酱能设计一个最小但完整的 Agent kernel。
2. Agent 的工具、上下文、敏感动作都能通过统一边界治理。
3. Agent 策略差异可以被 benchmark、trace 和 case card 解释。
4. 安全与上下文治理可以作为 agent 执行链路的一部分接受评测。

## 4. 非目标

- 不做完整 RAG 产品平台。
- 不做完整 Codex / Claude Code 替代品。
- 不做通用 guardrail SDK。
- 不做重 UI。
- 不承诺企业级安全效果。

## 5. 设计审稿期开放问题

1. 项目核心卖点应偏 Agent kernel、Agent eval、MCP protocol，还是 safety / context governance？
2. toy code repair 是否足够支撑 coding-agent-like 信号？
3. 是否需要引入真实开源 repo task，还是只做可控 fixture？
4. RAG pipeline 保留多少才不会稀释 Agent 主轴？
5. 是否值得在 W4 做 A2A reviewer handoff？


