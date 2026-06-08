# Design Review: ContextGuard Agent Lab

> Reviewer: 幽浮喵 (yufumiao)
> Date: 2026-06-08
> Phase: Phase 0 设计审稿期 — 骨架代码 + 设计文档审查

---

## Verdict

- **Go / Revise / Pivot**: **Revise** — 项目方向正确，但骨架代码与设计承诺之间有显著落差，需要收紧实现优先级再开 sprint。
- **Confidence**: 项目方向正确率 85%，当前骨架对算法岗信号强度 40%。

---

## Strongest Parts

### 1. 设计文档体系完整且有纪律
- `00-08` 九篇文档覆盖了 vision、architecture、claim contract、risk register、roadmap gates、background snapshot。
- Claim/eval contract 清晰区分了 allowed/disallowed claims，这对求职项目的诚实边界至关重要。
- Risk register 带有 kill/pivot criterion，说明项目有中途坍缩防线。

### 2. CaseSpec + ToolCallTrace + PolicyDecision schema 设计简洁但足够
- 三核心 dataclass（`CaseSpec`, `ToolCallTrace`, `PolicyDecision`, `RunRecord`）覆盖了评测工作台的数据闭环。
- ToolRegistry 的设计是 MCP-like 边界但无外部依赖，可以做 deterministic test。

### 3. EvidencePolicyEngine 逻辑正确且可评测
- 允许/阻断的证据契约是可测量、可追踪的，这是项目核心差异化之一。
- `unsafe_allow_rate` 和 `false_block_rate` 指标定义清晰。

### 4. 求职定位聚焦
- 项目主张收敛到 "Agent kernel + MCP tools + evidence policy + eval harness"，没有贪心做成 RAG 平台或通用 guardrail SDK。
- 与 AlgoCoach（后训练/eval）和 Loomstead（observability/trace）形成互补而非重复。

---

## Biggest Risks

### H1 — Agent kernel 只是 case_type router，无策略差异 [Critical]

**现状**：`AgentKernel.run()` 的核心逻辑是按 `case_type` 分支做硬编码处理。`strategy` 参数只是一个 label，不影响执行路径。

**影响**：
- 项目最核心的主张是 **"Agent 策略差异可以被 benchmark 解释"**（见 03_vision_and_positioning.md 第 3 点），但当前代码没有任何策略差异。
- 面试官问 "react_agent 和 guarded_agent 在同样的 case 上行为有什么不同"，目前无法回答。
- 这直接削弱 Agent 算法 / 应用策略算法岗位的信号强度。

**建议**：
- 策略差异不需要 LLM。最简单的起点是不同的 **deterministic planning policy**：
  - `react_agent`：直接 act，不 plan。
  - `plan_execute_agent`：显式生成 step list，再逐步执行。
  - `reflective_agent`：失败后做一次 observation-based retry。
  - `guarded_agent`：敏感动作前插入 evidence gate check。
  - `context_budget_agent`：设定 context window budget，超过则跳过低价值 retrieval。
- 每种策略应产生不同的 tool_calls 序列和不同的 success/metrics 结果。

### H2 — 无 reflection/repair loop 实现 [High]

**现状**：`kernel.py` 处理 toy_code_repair 时返回写死的字符串 `"repair_plan: inspect failure -> patch add(a, b) -> run tests"`，没有实际修复流程。

**影响**：
- 这是项目主张的核心之一（"可评测 Agent kernel: plan / act / observe / reflect / repair"），但当前是空壳。
- 面试官问 "agent 怎么从失败中恢复"，没有可演示的 trace。

**建议**：
- 最小实现：WorkspaceTools 已有 `list_files` 和 `read_file`。增加 `apply_patch` 和 `run_tests` 工具（可做 stub），让 reflective_agent 在失败后自动读取错误信息、尝试 patch、重跑测试。
- 不需要真跑 pytest——可以用一个 fixture 文件系统，`run_tests` 返回预设的 pass/fail。

### H3 — 3 个 sample case 全部 success=True，metrics 无区分度 [High]

**现状**：sample cases 只有 3 个，且 kernel 的硬编码逻辑保证它们全部 success。

**影响**：
- `task_success_rate` 恒为 100%，`unsafe_allow_rate` 恒为 0。
- 策略之间无差异，ablation 报告没有意义。
- 面试官问 "你的 ablation 实验展示了什么"，没有答案。

**建议**：
- 需要 **故意设计会失败的 case**：
  - RAG case：某些 query 无法用 keyword overlap 找到，react_agent 失败但 plan_execute_agent 通过多次 retrieval 成功。
  - Sensitive action case：有些 case evidence 只差一项，guarded_agent 正确 block，react_agent 错误 allow。
  - Code repair case：某些 bug 需要 2 次修复尝试，reflective_agent 修复成功但 react_agent 放弃。
- 目标：80-120 条总 case 中，至少 20-30% 在某些策略下失败。

### H4 — MCP 边界只有 manifest，无实际协议接入 [Medium]

**现状**：`mcp_server/server.py` 只返回 tool name 列表。README 说 "MCP-native" 但没有 FastMCP 或任何协议接入。

**影响**：
- "MCP-native" 是项目口号之一，但没有实现支撑。
- 如果面试官问 "MCP 在这个项目中具体指什么"，目前只能说 "我们用了类似 MCP 的 registry 抽象"。

**建议**：
- W2 实现 FastMCP adapter 至少暴露 retrieval 和 workspace 工具作为 MCP tool。
- 即使只有 2 个 tool 实际通过 MCP 暴露，也能证明 "MCP-native" 不是空话。
- 不要为了 MCP 而重构架构——ToolRegistry 已经是合理的抽象，只需要加 MCP 暴露层。

### H5 — context_budget_agent 完全空白 [Medium]

**现状**：5 种策略里只有 4 个在 `kernel._plan()` 有分支，`context_budget_agent` 没有任何设计。

**影响**：
- 这个策略对 "Agent 算法 / 应用策略算法" 岗位是最有信号价值的——它展示了 context 代价与检索收益的权衡思考。
- 但如果实现过于复杂，可能成为 scope trap。

**建议**：
- 最小实现：设定 token budget（可以是模拟的），`context_budget_agent` 在 retrieval 后评估 chunk 的估计价值，超过 budget 则截断。
- 关键是产出 **可比较的 metrics**（retrieval count vs success rate），而不是实现通用 context window 管理。

### H6 — Case family 覆盖不足 [Medium]

**现状**：
- RAG QA: 1 case（目标 30-50）
- Prompt injection: 0 case（目标 10-15）
- Retrieval poisoning: 0 case（目标 10-15）
- Sensitive action: 1 case（目标 20）
- Toy code repair: 1 case（目标 20-30）

**建议**：
- W1 至少每个 family 有 5 个 case，其中有意设计的 failure case。
- Prompt injection 和 retrieval poisoning 可以合并为一个 "adversarial context" family 以简化——这本就是关于 context 治理的。

### H7 — 报告质量不足展示求职价值 [Low-Medium]

**现状**：`sample_report.md` 只有 3 行表格。

**建议**：
- 报告应包含：
  - 策略 ablation 对比表（success rate / tool calls / unsafe allow / cost proxy）。
  - 3 张 case card（RAG、guardrail、code repair），每张展示完整的 tool calls trace 和 policy decision。
  - Bad case taxonomy（哪些 case 在什么策略下失败，为什么）。
- 这些才是面试时能拿出来说的东西。

---

## Missing Higher-level Role Signals

### 对 Agent 算法 / 应用策略算法岗位的信号缺口

1. **策略对比实验叙事**：当前没有 "为什么 react 不如 guarded" 的可展示结论。这是该项目最重要的求职叙事。

2. **Trace 可读性**：`ToolCallTrace` 存在但打印出来是 dataclass dict，没有人类可读的 timeline 视图。面试官需要 3 分钟内看懂一次 agent 执行的完整轨迹。

3. **Bad case 分析**：没有 "这个 case 为什么失败，reflective agent 怎么修复它" 的结构化叙事。

### 对 Agent 评测 / 安全护栏岗位的信号缺口

4. **Injection/poisoning case 缺位**：这是 context governance 的核心测试维度，但 0 case。

5. **Policy engine 过于简单**：当前 evidence gate 是精确匹配，没有模糊匹配、层级继承或可配置 severity。一个有 `severity: high` vs `severity: low` 的 policy 能展示更多工程深度。

---

## Over-scoped Parts to Cut (If Time)

| Module | 建议 | 理由 |
|---|---|---|
| A2A reviewer handoff | 从 W4 stretch 降为 Cut | 一月工期不需要，MCP 已足够展示协议边界 |
| Full MCP tool server (所有8个tool) | 保留 3-4 个核心 tool | export_data + search_docs + read_file + apply_patch 足够展示 |
| Real open-source repo tasks | 保持 Cut | fixture 修复任务足够展示 repair loop |
| Context budget 完整实现 | 降为 stub + metrics | 有 token threshold 模拟即可，不需要真实 token counting |
| Heavy UI | 继续保持 Cut | README + case card + markdown report 足够 |

---

## Recommended Final Scope

### Must-have (W1-W2)

1. **策略分化实现**：react / plan_execute / reflective / guarded 四种策略在相同 CaseSpec 上产生不同 tool_calls 和 metrics。
2. **EvidencePolicyEngine 进阶**：增加 evidence severity level 和 partial evidence 处理，让 guarded_agent 有更丰富的 decision trace。
3. **Reflection/Repair loop**：reflective_agent 在失败后重试，产出可追踪的 repair trace。
4. **15-20 个精心设计的 case**：每个 family 至少 5 个，含故意失败 case。
5. **策略 ablation 报告**：同一批 case 在 4 种策略上的对比表 + 3 张 case card。

### Should-have (W2-W3)

6. **FastMCP adapter**：至少 2 个 tool 通过 MCP 暴露，证明 "MCP-native" 不是空话。
7. **Adversarial context case family**：prompt injection + retrieval poisoning case，展示 context governance。
8. **context_budget_agent stub**：token threshold 模拟 + retrieval count vs success rate 的 tradeoff 表。
9. **Bad case taxonomy**：结构化的失败原因分类。

### Stretch (W3-W4)

10. **Workspace repair 完整闭环**：fixture workspace + apply_patch + run_tests。
11. **20+ toy code repair case**。
12. **Rich case cards**：包含 timeline 视图的 trace。

### Cut

- A2A platform implementation。
- Real open-source repo tasks。
- Full Universal tool server。
- UI work of any kind。

---

## Concrete Changes to Docs / Architecture / Eval

### D1 — AgentKernel 重构为策略模式

```text
现在: AgentKernel.run(case, strategy="guarded_agent") 
      → 按 case_type 分支，strategy 只是 label

应该: 
  class Strategy(Protocol):
      def plan(self, state) -> list[str]: ...
      def act(self, state, tools) -> ToolResult: ...
      def observe(self, state, result) -> None: ...
      def reflect(self, state) -> bool: ...  # True = retry
  
  class ReactStrategy(Strategy): ...  # no plan, direct act
  class PlanExecuteStrategy(Strategy): ...  # explicit plan then execute
  class ReflectiveStrategy(Strategy): ...  # retry on failure
  class GuardedStrategy(Strategy): ...  # evidence gate before sensitive action
  
  AgentKernel.run(case, strategy: Strategy)
```

这是项目最重要的架构变更。没有策略分化，ablation 就是空谈。

### D2 — 增加策略差异化 case

需要在 `data/benchmark/` 中增加以下类型的 case：

- **react 失败但 plan_execute 成功的 RAG case**：需要 multi-step retrieval。
- **unguarded 会 unsafe allow 但 guarded 正确 block 的 sensitive case**：同 action 不同 evidence。
- **需要 2 次 repair 尝试的 code case**：reflective 成功但 react 放弃。

### D3 — RunRecord 增加 reflection_steps

```python
@dataclass(slots=True)
class RunRecord:
    case_id: str
    strategy: str
    answer: str
    success: bool
    tool_calls: list[ToolCallTrace]
    policy_decisions: list[PolicyDecision]
    reflection_steps: list[str]  # 新增：记录 retry/repair 的决策轨迹
    metrics: dict[str, Any]
```

### D4 — Report 增加策略对比表模板

```markdown
## Strategy Ablation

| Strategy | Task Success | Mean Tool Calls | Unsafe Allow | False Block | Cost Proxy |
|---|---|---|---|---|---|
| react | ? | ? | ? | ? | ? |
| plan_execute | ? | ? | ? | ? | ? |
| reflective | ? | ? | ? | ? | ? |
| guarded | ? | ? | ? | ? | ? |
```

### D5 — EvidencePolicyEngine 增加 severity 和 partial match

```python
@dataclass
class EvidenceRequirement:
    action: str
    required_evidence: list[str]
    severity: str = "high"  # high / medium / low
    partial_allow_threshold: float = 1.0  # 1.0 = 必须全部具备
```

这能让 guarded_agent 产生更丰富的 policy decision trace（block/high-severity vs allow-with-warning/low-severity）。

### D6 — Roadmap 调整建议

```text
原 Phase 1: Deterministic agent baseline
  → 改为: 策略分化 + failure case design

原 Phase 2: Strategy ablation
  → 合并到 Phase 1，因为策略分化是 baseline 的一部分

原 Phase 3: Workspace repair loop  
  → 保持，但降低 case 数量目标到 10+
  
原 Phase 4: MCP and case cards
  → 保持，MCP 简化为 2-3 个 tool 暴露
```

---

## Summary

项目设计方向正确，claim contract 和风险控制有纪律。**但骨架代码目前是一个 case_type 路由器而非 Agent kernel**。最关键的单一改动是引入策略模式让不同策略产生不同行为和 metrics——这是 Agent 算法岗位的核心信号，也是 ablation 报告的灵魂。

建议 Phase 0 gate 增加条件：**至少 2 种策略在相同 case 上产生不同的 tool_calls 序列和 success 结果**。

---

*Review by 幽浮喵 | 2026-06-08*