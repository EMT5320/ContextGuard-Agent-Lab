# Review: ContextGuard Agent Lab（新版 pivot 方案）

> Reviewer: 幽浮喵 / 浮浮酱 (Cascade)
> Date: 2026-06-09
> 审阅对象：codex 收束后的新版方案 `MCP-compatible Agent Strategy Benchmark`
> 输入：`docs/design/00-09`、`docs/review/00-01`、`docs/review/reviews/{5.5pro,GLM5.1,OPUS4.8}`、`src/contextguard_agent_lab/**`、目标岗位现状调研
> 说明：这是**第一份针对新版 pivot 方案**的 review。前三轮 review 主要基于旧版 `evidence-governed workbench`，结论仍有参考价值，但定位部分已部分过时。
> 状态：本文仅记录意见，未做最终决策。主人将综合考虑后再拍板。

## Verdict

- 判断：**方向健康，设计已收敛；继续做。但存在一个未被前三轮点透的"信号-岗位错配"隐患，需在拍板主轴时正视。**
- 置信度：中高。
- 一句话：设计层面 codex 已收敛得很干净，工程隐患照 roadmap 补即可；真正需要决策的是 ContextGuard 对"Agent 算法岗"的信号到底要做到多强。

## 1. 现状确认：设计已收敛 vs 代码未落地

### 设计层面（健康）

- 主轴从旧版 `evidence-governed workbench` pivot 到 `MCP-compatible Agent Strategy Benchmark`，核心为 `AgentStrategy ablation + ToolSpec/ToolExecutor + context budget + verification + success-cost frontier`。
- 作品集分工清晰：AlgoCoach 扛 post-training/verifier/eval infra；Loomstead 扛 observability/trace/replay；ContextGuard 补 MCP tool boundary + 策略评测 + context 治理的公开缺口。
- 工程纪律强：claim/eval contract、risk register（含 kill criteria）、roadmap gates 完整。

### 代码层面（宣称领先实现，三轮 review 批评尚未落地）

| 能力 | 设计宣称 | 代码现状 | 位置 |
|---|---|---|---|
| AgentStrategy 接口 | 策略可插拔、控制流分化 | `strategy` 仅是 label，`kernel.py` 按 `case_type` 分支 | `agents/kernel.py:23-86` |
| 独立 grader | success 判定独立于控制环 | success 内嵌在 kernel | `kernel.py:37,52,71` |
| 报告指标 | family + strategy 多指标 | `generate_report.py` 绕过 `metrics.summarize` | `eval/metrics.py`、`scripts/generate_report.py` |
| ToolSpec | name/schema/risk/cost/mcp 元数据 | 只有 `ToolRegistry`，无 `ToolSpec` | `tools/registry.py` |
| repair loop | fixture + apply_patch + run_tests | 写死 `success=True` | `kernel.py:63-73` |
| MCP-compatible | FastMCP adapter | 仅静态 manifest | `mcp_server/server.py` |

结论：README 已诚实标注 design-review phase，因此这些是"待执行"而非"设计错误"。

## 2. 保留的强项（无异议，照做）

- **pivot 决策正确**：避开 Loomstead 重合，救了作品集叙事。
- **claim-evidence 纪律是稀缺优势**：反向防止过度包装，面试好防守。
- **deterministic-first 正确**：可复现、现场能跑。
- **三轮 review 的工程修复清单正确**：AgentStrategy 接口、独立 grader、family+strategy 报告、MCP-compatible 措辞、repair 不要 stub success——照 roadmap 执行即可。

## 3. 核心隐患：信号与"Agent 算法岗"的结构性错配

主人的最终目标是冲更高级的 **Agent 算法岗**。结合目标岗位现状调研，必须诚实指出一个三轮 review 都未点透的问题：

### 岗位现状（调研结论）

- 国内 Agent 岗位明确分两条线（来源：AgentGuide，基于大厂真实 JD）：
  - **算法工程师线**：评价标准 = 算法创新 + 指标提升(+X%) + 消融实验 + baseline 对比 + 论文/开源影响力。最热细分是"上下文工程算法"（RAG算法 / Agent Memory / 规划算法 / Multi-Agent）和"模型算法"（Reasoning RL、RLHF/DPO/GRPO）。
  - **开发/应用工程师线**：评价标准 = 完整系统 + 业务指标 + 性能优化 + 工程能力。
- 2025-2026 Agent 算法岗最核心趋势是 **Agentic RL**：把 LLM 当作可学习策略，用 RL（GRPO/PPO）+ multi-turn rollout 提升 reasoning/tool use/memory/planning（NeurIPS 2025 workshop、多篇综述共识）。

### 对照 ContextGuard

- ContextGuard 目前是 **deterministic（规则）策略的工程化对比工作台**，**没有 learning、没有 trained policy、没有算法创新点**。
- 因此：
  - 对 **Agent eval / Context Engineering / 应用策略** 岗位信号**很强**。
  - 对 **Agent 算法工程师**（主人想冲的更高级岗）只证明"会设计评测、会做工程对比"，**不证明"能提出新算法并用消融证明它更好"**。算法岗面试官会问"你的策略都是已知的，算法贡献在哪"，当前设计答不上来。

### 性质

这不是设计错误，而是**期望与设计的潜在错配**：

- 若指望 ContextGuard **单独**把主人推上 Agent 算法岗 → 它缺一个"可量化的算法创新内核"。
- 若 ContextGuard 定位为冲 Agent **应用策略 / eval** 岗，AlgoCoach 扛算法岗 → 当前方向完全正确。

## 4. 工程隐患（三轮 review 共识，代码层面尚未修复）

按严重度排序，照 roadmap 补即可：

1. **kernel 名实不符**（最致命）：`strategy` 是 label，无策略分化 → ablation 会"全相同"。对应 R2。
2. **eval validity**：success 判定内嵌 kernel（自评），report 绕过 metrics → 易被攻击。对应 R4/R5。
3. **repair stub success=True**：公开报告里会被一击打穿。
4. **MCP 只是 manifest**：README 顶部词汇负债。
5. **缺独立 grader / ToolSpec / family 报告**。

## 5. 愿景：四条可能走向

| 路线 | 内容 | 岗位信号 | 风险 |
|---|---|---|---|
| **A 稳守 eval/应用策略** | 保持 deterministic benchmark，仅补工程隐患 | Agent eval / Context Engineering / 应用策略（upward） | 最低，但算法岗信号弱 |
| **B Agentic RL 训练-评测环境** | ContextGuard 提供 tool env + CaseSpec + reward，AlgoCoach 做 RL 训练可学习策略，形成训练↔评测闭环 | 直击 Agent 算法岗 + 模型算法岗 | 高，工期大、与 AlgoCoach 强耦合 |
| **C 轻量 learned 策略内核** | deterministic 之上加一个 learned 组件（如 learned tool/budget router，bandit/轻量 policy learning），做消融证明优于固定策略 | 制造一个可量化算法创新点 + 指标提升 + 消融，从评测工作台升级为"评测+小算法贡献" | 可控，性价比最高 |
| **D 暂缓 ContextGuard** | 集中火力做厚 AlgoCoach 的 RL/post-training 信号，ContextGuard 设计冻结 | 避免两个项目互相稀释 | 取决于时间紧迫度 |

浮浮酱倾向：若时间允许，**C 是性价比最高的折中**（用最小代价补上算法信号）；**B 是天花板最高**但需与 AlgoCoach 统筹；A/D 取决于时间与精力分配。

## 6. 需主人澄清的事实点（影响路线选择）

- **求职时间线 / 紧迫度**：几周内冲刺，还是有 2-3 个月窗口？
- **AlgoCoach 当前阶段**：P0 证据收口了吗？两个项目精力如何分配？（OPUS4.8 反复警示的 R7 时间冲突）
- **目标公司类型**：国内大厂研究院 / 头部模型创业（月暗、智谱、MiniMax、DeepSeek 类）/ 海外？对论文/开源 stars 的硬要求差异大。
- **论文/开源诉求**：是否打算发论文或刷开源影响力？算法岗硬通货，影响 ContextGuard 是否值得做成"可发表的小研究"。

## 7. 待主人后续拍板的决策点

1. **ContextGuard 主轴方向**：A / B / C / D（见第 5 节）。
2. **ContextGuard 与 AlgoCoach 的耦合度**：独立项目，还是组成"训练-评测"组合拳？
3. **时间优先级**：与 AlgoCoach P0 的排序（R7）。
4. **算法信号来源**：靠 ContextGuard 自带算法内核，还是完全交给 AlgoCoach？

## 8. 调研来源

- AgentGuide（国内 Agent 岗位两条线分析，基于大厂真实 JD）：https://github.com/adongwanai/AgentGuide
- Agentic RL 综述（The Landscape of Agentic Reinforcement Learning, 2509.02547）。
- A Practitioner's Guide to Multi-turn Agentic RL（2510.01132，NeurIPS 2025 workshop）。
- Evaluation and Benchmarking of LLM Agents: A Survey（KDD 2025, 2507.21504）。

---

> 使用建议：本文与前三轮 review 对照。前三轮的工程修复清单已被 codex 收束进设计文档，可直接执行；本文新增的"信号-岗位错配"与"四条愿景路线"留待主人综合 AlgoCoach 进度与求职时间线后决策。任何被接受的修改都应映射回 `05_claim_and_eval_contract.md`。
