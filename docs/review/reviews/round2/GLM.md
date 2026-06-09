ContextGuard Agent Lab 综合审稿报告
Verdict: Go, 但需要在三个维度做硬收敛
项目方向正确且有价值——"MCP-compatible Agent Strategy Benchmark"确实填补了公开作品集的核心缺口。三份 review 的一致判断（Revise / Go-but-revise）也是对的。但浮浮酱在所有 review 的基础上，要指出几个尚未被充分讨论的结构性问题喵～
一、当前设计合理性的正面判断
1. Pivot 方向正确：从 evidence-governed workbench 转向 Agent Strategy Benchmark，成功避开与 Loomstead 的 observability/audit 主线重合。这是项目存在的合法性基础。
2. Claim/Eval Contract 是差异化：05_claim_and_eval_contract.md 对"允许/禁止声明什么"做显式约束，这个工程纪律本身就是面试强信号——很多候选人只会"做得越多越好"，缺少 scope discipline。
3. 设计文档体系已超越大多数 portfolio 项目：从 background snapshot、risk register（含 kill criterion）、overlap audit 到 review packet，这套"先约束后实现"的思路对 Agent eval 岗位非常对味。
4. 与已有作品的分工是清晰的：AlgoCoach 扛 post-training/eval infra，Loomstead 扛 observability/replay，ContextGuard 扛 strategy ablation + tool boundary + budget frontier——三件作品叙事互补、不重叠。
二、所有 review 都指出但仍未解决的核心问题
三份 review（Cascade、GLM5.1、5.5pro）高度一致地指出了 4 个问题，浮浮酱认为这些是项目成败的关键：
问题	所有 review 的一致判断	当前状态
Kernel 是 case_type router，strategy 只是 label	必须重构成 AgentStrategy 接口	kernel.py 仍按 case_type 分支
MCP-native 只是 label	至少降级措辞或做最小 FastMCP	mcp_server/server.py 只返回 manifest
toy_code_repair stub 成功	不能公开呈现 success=True	kernel.py:71 写死 success=True
eval validity 可被攻击	需独立 grader	success 判定嵌在 kernel 分支里
浮浮酱的判断：这 4 个问题在 pivot 后的设计文档里虽然已经被承认（honest boundaries 等），但代码还没有跟进。下一个 sprint 必须优先解决前两个，否则项目的核心主张（strategy ablation + MCP-compatible）立不住。
三、现有 review 未充分讨论的结构性隐患
3.1 "Strategy Benchmark" vs "真实 LLM Agent" 的张力
所有 5 个 starter strategy（react / plan_execute / verify_then_answer / reflective / context_budget）都用确定性规则实现，不依赖 LLM。这在 MVP 阶段是正确的。
隐患：Agent 算法岗位的面试官会问——"你的策略差异来自硬编码规则还是来自模型决策？" 如果全部是规则分支，ablation 展示的只是"不同 if-else 分支的效果"，而不是"Agent 控制策略的本质差异"。
浮浮酱的建议：
- MVP 先用确定性策略把 ablation pipeline 跑通，这没问题。
- 但 Phase 3 之后必须有 LLM-backed 策略的对比实验——哪怕只接一个 cheap model（如 Qwen3-4B / GLM-4-Flash）做 planner，展示"规则策略 vs LLM 策略"的 success-cost 差异。这才是 Agent 算法岗位要看的信号。
- 否则项目信号更偏 Agent 工程而非 Agent 算法。
3.2 "MCP-compatible" 的价值锚点不够锋利
当前设计把 MCP 定位为"工具协议边界"——ToolSpec / ToolRegistry / ToolExecutor 镜像 MCP 的结构化 schema。但：
- 2025 年的 MCP Safety Audit 论文（arXiv:2504.03767）已经指出 MCP 存在 prompt injection、恶意工具调用、credential theft 等安全问题。
- 2026 年的 MCP Production Patterns 论文（arXiv:2603.13417）指出 MCP 还缺少 identity propagation、adaptive tool budgeting、structured error semantics 三个生产级原语。
浮浮酱的建议：
- 不需要实现完整的 MCP 安全审计框架，但项目应该有意设计 2-3 个 case 展示 MCP 工具边界的攻击面——例如 adversarial context case 里，distractor doc 试图让 agent 调用不该调用的 sensitive tool。这样 "MCP-compatible tool boundary" 就不只是"用了类似 MCP 的 schema"，而是"在 MCP 边界上评测了策略安全性"。
- 这与 arXiv:2603.13417 的 "adaptive tool budgeting" 直接对齐——你的 context_budget_agent 就是 tool budget 的一种实现，可以在 README 里引用这篇论文作为 motivation。
3.3 Case Quality 比 Case Quantity 更重要——但 "20-30% 失败率" 的设计原则需要更具体的指导
设计文档说"至少 20-30% cases 应让某些策略失败"，但没说怎么设计这些 case。
浮浮酱的建议：case design 应该围绕 策略差异维度 构建，而不是围绕"任务类型"构建：
差异维度	Case 设计原则	失败触发条件
检索深度	需要 2+ hop retrieval 才能找到 gold doc	react 只搜 1 次，plan_execute 搜 2+ 次
验证时机	答案必须由 citation 支持，否则算 unsupported	verify_then_answer 会验证，react 不会
预算约束	context window 不够放下所有检索结果	context_budget 截断低价值 chunk，可能错过关键信息
对抗干扰	检索结果中有 poisoned/distractor doc	react 会被 distractor 误导，verify 策略能检测
反思修复	第一次修复失败，需要第二次尝试	reflective 会 retry，react 放弃
这样每个 case 不是"某个类型"，而是"某几个差异维度的组合"。ablation 报告才能回答"哪个维度对成功率影响最大"。
3.4 作品集叙事的"三维证据"还不够立体
当前三个项目的叙事分工：
项目	主信号	缺少什么
AlgoCoach	后训练 + eval + data flywheel	Agent 运行时 / 工具使用
Loomstead	Observability + trace + audit	策略对比 / 成本权衡
ContextGuard	策略 ablation + tool boundary + budget	算法创新（目前只有工程 pattern）
核心问题：ContextGuard 目前展示的是"浮浮酱主人能设计评测"，但还没展示"浮浮酱主人能发明算法"。Agent 算法岗位不只是看你能做 eval，还要看你是否能提出新的策略或改进。
浮浮酱的建议：
- context_budget_agent 不应该只是一个"截断低价值 chunk"的规则，应该引入一个简单的value-of-information 估计——即使是最简单的启发式（如"chunk 与 query 的相关性分数 × 剩余预算比例"），也比纯截断更像"算法"。
- 在 ablation 报告里，要有一节**"Why context_budget_agent works (or doesn't)"**，解释 budget 策略背后的信息论/决策论直觉。这比单纯列 metrics 有深度得多。
四、未来愿景讨论
浮浮酱认为这个项目有三层可能的未来愿景，按信号强度排序：
愿景 A：Agent Strategy Benchmark（当前主轴）
"同一批 cases 下，不同 Agent 策略如何因 tool boundary、evidence gate、reflection 和 context budget 产生不同结果。"
- 信号强度：中等。展示工程纪律 + eval 能力，但偏"评测"而非"算法"。
- 适配岗位：Agent engineer / Agent eval / Context engineering。
- 风险：如果 strategy 全是规则，面试官会认为"这不是 algorithm 而是 if-else"。
愿景 B：Cost-Aware Agent Control Policy（升级方向）
"Agent tool use is a control policy under budget constraints; the right policy depends on task structure, evidence quality, and cost tolerance."
- 信号强度：高。把 "strategy" 升格为 "control policy"，引入 budget / cost / value-of-information 的决策论视角，面试官看到的不再是"比较几个规则"，而是"用有限预算做最优决策"。
- 适配岗位：Agent algorithm / Application strategy algorithm。
- 实现路径：
1. context_budget_agent 升级为基于 VoI 估计的 budget policy。
2. 引入 success-cost frontier 的帕累托分析——哪些策略在哪些 case 上帕累托占优。
3. 报告从"leaderboard"升级为"policy recommendation under different cost tolerance"。
- 引用支撑：arXiv:2603.13417 的 "Adaptive Timeout Budget Allocation" 直接对标。
愿景 C：MCP-Governed Agent Evaluation（长期愿景）
"在 MCP 工具生态的安全边界上评测 Agent 策略，包括 prompt injection 防御、evidence gate、tool budget 和 identity propagation。"
- 信号强度：极高（但实现量大）。直接对齐 MCP 安全审计和 MCP 生产部署的前沿问题。
- 适配岗位：Agent algorithm + Agent 安全 + MCP 生态。
- 实现路径：需要在愿景 A/B 之后，增加 adversarial MCP case、identity-aware tool call、structured error recovery。
- 风险：scope 容易膨胀，需要严格的 phase gate。
浮浮酱的建议：短期执行按 愿景 A → B 的路径走，让 context_budget_agent 和 success-cost frontier 成为算法信号的锚点。愿景 C 作为"项目未来方向"写在 README 的 Roadmap 一节，展示主人有前瞻视野但不会现在就膨胀 scope。
五、几个需要主人确认的问题
1. 主人的 AlgoCoach-Flywheel 和 Loomstead 当前分别处于什么阶段？ 如果 AlgoCoach P0 还在进行中，ContextGuard 的优先级和时间分配需要明确。浮浮酱目前假设两者可以并行推进。
2. 主人对"接 LLM 做策略对比"的态度？ 浮浮酱认为 Phase 3 之后至少需要一个 LLM-backed 策略（哪怕用便宜模型），否则算法岗信号不够。但接 LLM 会引入非确定性，需要考虑 eval validity 如何保证。
3. 主人目前的面试时间线？ 如果 1-2 个月内需要用这个项目面试，那 scope 必须进一步收缩——MVP 到愿景 A 就够了。如果时间更充裕（3-4 个月），可以推进到愿景 B。
4. 主人的 Loomstead 里有 coding dry-run 的 secondary validation，ContextGuard 的 coding fixture 是否还需要保留？ 三份 review 对此意见不一，浮浮酱倾向 Phase 1-2 先砍掉，Phase 3 根据带宽决定。
六、总结：接下来最该做的 5 件事
1. 重构 kernel → AgentStrategy 接口：这是项目存在意义的根基，没有策略分化就没有 ablation。
2. 实现 ToolSpec + ToolExecutor：让 MCP-compatible tool boundary 有实际 schema 支撑，不是空话。
3. 砍掉 toy_code_repair 的 success=True：改成 success=False + reason="repair_loop_not_implemented"，公开 report 不能有 stub 成功。
4. 设计 10-15 个围绕策略差异维度的 case：不是围绕"类型"，而是围绕"什么情况下不同策略会分化"。
5. context_budget_agent 从简单 VoI 启发式开始：让它不是"截断"而是"选择"，这是从工程升级到算法的关键一步。