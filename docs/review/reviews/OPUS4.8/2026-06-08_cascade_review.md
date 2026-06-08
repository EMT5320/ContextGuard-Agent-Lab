# Review: ContextGuard Agent Lab

> Reviewer: Cascade（幽浮喵）
> Date: 2026-06-08
> Inputs: `docs/design/00-08`, `docs/review/00-01`, `src/contextguard_agent_lab/**`, `data/**`, `reports/**`
> Review lens: 愿景与岗位价值、技术可行性、claim-vs-artifact 一致性、评测有效性、范围收敛

## Verdict

- Go / revise / pivot: **Revise**。方向成立且差异化清晰，但当前 claim 明显领先实现，需要在 kernel、repair loop、MCP 三处补上真实证据，并对范围做一次硬收敛。
- Confidence: 中高。设计文档与治理纪律已是强信号；主要风险集中在"宣称的能力尚未在代码中兑现"。

## 1. 现状快照：宣称 vs 实现

| 能力 | 文档宣称 | 代码现状 | gap |
|---|---|---|---|
| Agent kernel loop | plan / act / observe / reflect / repair | `kernel.py` 是按 `case_type` 的 if-else 分发，无 observe/reflect/repair 节点 | 高 |
| 5 种 strategy | react / plan_execute / reflective / guarded / context_budget | `strategy` 仅被记录，不改变控制流，跑出来结果相同 | 高 |
| Workspace repair loop | fixture + apply_patch + run_tests + 重跑 trace | `kernel.py:66-72` 返回硬编码字符串且 `success=True` 写死；`workspace.py` 只有 `list_files`/`read_file` | 高 |
| MCP-native | FastMCP 暴露 retrieval/workspace 工具 | `mcp_server/server.py` 仅返回静态工具名 manifest，无任何协议实现 | 高 |
| Evidence-gated execution | 证据契约 + allow/block/review + 审计 trace | `policy.py` 真实可跑，目前只有 block 路径被验证 | 低 |
| 评测指标契约 | 7 个 metric（success / tool / repair / unsafe_allow / false_block / evidence_coverage / cost_proxy / latency） | `metrics.py` 仅 4 个，且 `generate_report.py` 根本没调用 `summarize`，report 只数 success | 中高 |
| Case families | rag_qa / injection / poisoning / sensitive / code_repair | kernel 只处理 3 类，injection/poisoning 落到 `unsupported case type` | 中 |
| 工具清单 | README 列出 `read_doc`/`verify_citation`/`search_repo`/`apply_patch`/`run_tests`/`delete_record`/`change_policy` | 代码中均未实现 | 中 |

**结论**：骨架是"可复现的确定性 baseline + 完整治理文档"，但 README 顶部的 `MCP-native, evidence-governed agent evaluation workbench` 三个核心词里，目前只有 `evidence` 有真实代码支撑。

## 2. Strongest parts

- **治理文档体系本身就是强信号**：claim/eval contract、risk register（含 kill criteria）、background snapshot、multi-model review packet——这套"先立约束再写代码"的工程纪律，对 Agent eval / 应用策略岗位非常对味。
- **EvidencePolicyEngine 是真实差异点**：`policy.py` + `policies.json` 的 required/observed/missing 证据契约可跑、可测、可解释，且与市面普通 guardrail demo 拉开差距。
- **确定性、无 LLM 依赖的 baseline**：fresh clone 即可 `unittest` + 生成 trace/report，复现性好，便于面试现场演示。
- **统一 CaseSpec + JSONL trace + report 链路**：schema 小而显式，`RunRecord`/`ToolCallTrace`/`PolicyDecision` 结构清晰，为后续 ablation 留了正确的地基。

## 3. Biggest risks

1. **Kernel 名实不符（最致命）**：宣称 plan-act-observe-reflect-repair + 5 strategy，实际是 case 分发。后果是 strategy ablation 会"全相同"，而 ablation 正是上探 Agent algorithm / 应用策略算法岗位的核心证据。对应 risk register R2。
2. **MCP 只是 label**：README 大字 `MCP-native`，但 `mcp_server` 无协议实现。面试官一句"演示一下你的 MCP server"即可击穿。这是公开展示项目里风险收益最不对称的一处。
3. **repair loop 造假**：`success=True` 写死 + 硬编码 repair_plan 字符串，且没有 `apply_patch`/`run_tests`。claim contract 中"Workspace repair loop is demonstrated on bounded fixtures"目前没有任何证据，对应 R4。
4. **评测有效性可被攻击**：success 判定逻辑内嵌在 `kernel.py`（如 `kernel.py:37` 与 `kernel.py:71`），等于"被测者自己给自己打分"。`generate_report.py` 又绕过了 `metrics.py`。这正是 R5（eval lacks validity）的现实化。
5. **dangling claims**：injection/poisoning case family、README 工具清单、7 个 metric 中的多数，都"写了但没接路径"。公开仓库里"承诺未兑现"比"范围小"更伤可信度，对应 R6。
6. **范围 vs 时间 + AlgoCoach 竞争**：当前一个月目标（80-120 case / 20+ repair / 4+ strategy / MCP / 多 report / case cards）偏大，叠加 R7（与 AlgoCoach P0 抢时间），有中途坍缩风险。

## 4. Missing higher-level role signals（上探岗位还缺的硬证据）

- **策略真差异**：reflection 真的能把一个失败 case 修复成功；context budget 真的影响 success/cost；ablation 表里出现可解释的 tradeoff，而不是同一行复制四遍。
- **真实 repair 闭环**：读失败测试 → 生成/应用 patch → 重跑 → trace 记录失败与成功，哪怕只有确定性规则修复器。
- **eval validity 工程**：独立 grader、bad-case taxonomy、指标反作弊说明（哪些 metric 容易被刷、如何防）。
- **协议边界落地**：哪怕只有一个 FastMCP server 真实暴露并被 kernel 调用一个工具，"protocol-native"才成立。

## 5. Over-scoped parts to cut

- **case family 5 → 3**：主线只留 `rag_qa` / `sensitive_action` / `toy_code_repair`；`prompt_injection` / `retrieval_poisoning` 降级为 rag 的 adversarial 子集或 stretch。
- **strategy 5 → 3**：保留行为真有差异的 `react` / `reflective(repair)` / `guarded`；`plan_execute` 与 `context_budget` 降级为 stretch。
- **README 工具清单**：未实现的工具名先从 README 移除或标注 planned，避免 dangling claim。
- **A2A**：维持 stretch（现状正确，不动）。

## 6. Recommended final scope

- **Must-have**
  - 真 kernel loop：抽出 `Strategy` 接口（plan/step/observe/should_continue），策略只改变控制流、不改变工具语义。
  - 真 repair loop：`fixtures/` 放可跑 toy repo（带失败测试）+ `apply_patch` + `run_tests`，repair 成功由真实 test 退出码判定。
  - evidence gate 补全：补 allow 正例与 `false_block` 反例，覆盖 block/allow/review 三条路径。
  - 独立 evaluator：把 success/scoring 从 kernel 抽到 `eval/grader.py`，case 自带 expected outcome + grader 类型。
  - strategy ablation report：≥3 strategy 跑同一批 case，展示 success/tool_calls/cost/latency 差异。
  - 3 张 case card：RAG、guardrail、code repair。
- **Should-have**
  - 一个最小 FastMCP server 真实暴露 `search_docs` + `read_file` 并被 kernel 调用。
  - `cost_proxy` 与 `latency` 真实测量（当前 `latency_ms` 恒为 0）。
  - bad-case taxonomy（按失败模式归类的坏样本集）。
- **Stretch**
  - injection/poisoning adversarial 子集与最小检测。
  - `context_budget` 实验。
  - A2A reviewer handoff。
- **Cut**
  - 通用 RAG 平台、向量库 plumbing、重 UI、大型 guardrail 规则库、Codex/Claude Code 全量替代。

### 修订版 phase 计划（与现有 `07_roadmap_and_gates.md` 对齐微调）

| Phase | 目标 | 退出 gate |
|---|---|---|
| P1 重构 kernel | Strategy 接口化 + 独立 grader + latency 真实计时 | 同一 case 下 react 与 guarded 控制流可见差异；grader 与 kernel 解耦 |
| P2 repair 闭环 | fixtures + apply_patch + run_tests + reflective 修复 | 至少 1 个 fixture 从 fail→fix→pass 全程有 trace |
| P3 ablation | ≥3 strategy 跑统一 case + 真实 metrics 进 report | report 由 `metrics.summarize` 驱动，含 ≥3 bad case |
| P4 MCP + case cards | 最小 FastMCP + 3 张 case card + README claim 对齐 | "MCP-native" 有可演示证据，README 标注 implemented/planned |

## 7. Concrete changes to docs / architecture / eval

- **architecture**：在 `agents/` 下新增 `strategy.py`（`Strategy` 基类 + react/reflective/guarded 子类），`kernel.py` 退化为驱动循环；`AgentState.observations/evidence/scratchpad` 真正被写入。
- **eval**：新增 `eval/grader.py`，success 判定按 case_type 多态化；`generate_report.py` 改为调用 `metrics.summarize` 输出 7 指标表，而非自行数 success。
- **tools**：`workspace.py` 补 `apply_patch`/`run_tests`/`search_repo`；`tools/sensitive.py` 落地 mock 敏感动作并强制经过 policy gate。
- **mcp**：要么落地最小 FastMCP，要么把 README/文档措辞降级为 `MCP-style boundary (FastMCP adapter in progress)`，二选一，不可悬空。
- **docs**：新增 `docs/design/09_mvp_cut_line.md` 固化 Must/Should/Stretch/Cut；README 增加"能力状态矩阵"（implemented / in-progress / planned）。
- **claim contract**：为每条 allowed claim 标注当前证据状态（done / partial / todo），形成可追踪的 claim-evidence 映射。
- **data**：sample case 从 3 条扩到每类 ≥3 条，便于 ablation 出现非平凡差异。

## 8. 需要主人拍板的决策点

1. **核心卖点单一化**：偏 `Agent kernel + strategy eval`（上探算法岗）还是 `evidence-gated execution + protocol boundary`（稳守应用/安全岗）？建议二选一作为 README 第一句主轴。
2. **MCP 取舍**：本期真做最小 FastMCP，还是降级措辞、把 MCP 放 stretch？
3. **repair loop 深度**：确定性规则修复器即可，还是要接 LLM 修复（引入模型依赖与不确定性）？
4. **与时间冲突**：本项目与 AlgoCoach P0 的优先级如何排（R7）？

### Reviewer 倾向（供后续讨论，非定论）

- **决策点 1（核心卖点）**：短期执行先按"暂不定主轴"——理由是现在 kernel 还没有真实策略差异，过早定"主轴是不是 kernel eval"缺乏数据支撑；先做 P1 重构让策略行为可区分，P3 的真实 ablation 会自然告诉你哪个方向更有说服力。但**长期主轴倾向"Kernel + 策略评测"**：AlgoCoach 已扛 post-training/eval infra，Loomstead 已扛 observability/replay，公司经验已扛 guardrail/RAG/安全——"可评测、可对比、可现场演示的通用 Agent kernel + strategy ablation"是唯一没被现有 asset 覆盖、且天花板最高的公开缺口。governance 留作差异化辅料即可，单独作主轴会与公司安全经验 + Loomstead 高风险拦截重叠（R3）、公开新意有限。
- **决策点 2（MCP）**：倾向"本期真做最小 FastMCP"。哪怕只暴露 `search_docs` + `read_file` 两个工具被 kernel 调用，"protocol-native"就立住了；ROI 极高，且能把 README 顶部的 `MCP-native` 从负债变资产。若实在没时间，则必须先降级措辞，不能悬空。
- **决策点 3（repair 深度）**：倾向"先确定性规则修复器"。先用规则修复器把 fail→fix→pass 的 trace 闭环跑通、指标可信，再把 LLM 修复作为 stretch 叠加；避免一上来引入模型不确定性污染 eval validity。
- **决策点 4（时间冲突）**：若 AlgoCoach 仍在 P0，建议 ContextGuard 本阶段只推进 P1（kernel 重构 + 独立 grader），其余 phase 排到 AlgoCoach P0 证据收口之后，严守 R7 的 kill criterion。

## 9. 其他意见

- **3 分钟可读性**：README 顶部加一张架构图 + 一句电梯陈述 + 指向"最强 case card"的链接，面试官前 3 分钟的体验决定第一印象。
- **与 Loomstead 显式区分**：一句话讲清边界——ContextGuard = 事前 evidence gate + protocol boundary + strategy eval；Loomstead = 事后 observability + replay。否则易被当作重复造轮子。
- **诚实边界已做得好**：README 的 honest boundaries 是加分项，保持；补实现时同步更新即可。
- **进度纪律**：建议加一个轻量 `progress.txt` 跟踪 phase gate 勾选状态，避免多 session 重复决策。

---

> 使用建议：本 review 不是最终真理。请与其他模型 review 对照分歧，并把每一条接受的修改映射回 `05_claim_and_eval_contract.md` 的 claim-evidence 表。
