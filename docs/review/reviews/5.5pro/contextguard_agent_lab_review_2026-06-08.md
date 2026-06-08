# Review: ContextGuard Agent Lab

> 审阅日期：2026-06-08  
> 审阅对象：`EMT5320/ContextGuard-Agent-Lab` 当前设计文档与初始实现骨架  
> 建议放置位置：`docs/review/02_portfolio_project_review_2026-06-08.md`

## Verdict

- Go / revise / pivot：**Go, but revise scope and claim wording before heavy implementation.**
- Confidence：**0.78**
- 总判断：项目方向值得继续。它能补齐公开作品集中“标准工具边界、Agent kernel、策略评测、evidence-gated execution、workspace repair loop”的缺口。当前设计已经比普通 RAG demo / guardrail demo 更像一个可讲清楚的求职展示项目；主要风险在于愿景太满、MCP-native 与 coding-agent-like 两个词容易被追问、策略 ablation 如果只是规则分支会显得薄。

## Strongest parts

1. **岗位画像对齐清楚。** 项目明确服务于 Agent 工程、大模型应用、Agent 算法 / 应用策略算法、Agent 评测 / 安全护栏岗位，且与公司经验、AlgoCoach、Loomstead 的分工已经写清楚。

2. **主张有辨识度。** “Agent kernel + MCP-style tools + evidence policy + strategy ablation + trace/report/case cards”比“做一个 RAG 平台”更适合公开作品展示。

3. **claim contract 是强项。** 项目已经把 allowed claims、disallowed claims、required evidence、minimum metrics 单独文档化，这能防止 README 过度包装，也有利于面试时防守。

4. **当前实现选择正确。** 依赖很轻，先跑 deterministic starter，先生成 JSONL trace 和 Markdown report。对 portfolio 项目来说，可复现入口比“漂亮但跑不起来”的复杂系统更重要。

5. **风险意识足够早。** 风险登记表已经识别 RAG 平台化、Agent kernel 太浅、guardrail 重复公司经验、coding-agent 范围膨胀、eval validity 不足等问题。

## Biggest risks

### R1. “MCP-native”目前容易被质疑为标签化

当前 ToolRegistry 确实采用了结构化 arguments / payload / trace 的边界，但还没有真实 MCP server、tool schema、capability metadata、transport 层或 FastMCP adapter。因此近期更稳妥的公开措辞是：

```text
MCP-style / MCP-compatible tool boundary first; FastMCP adapter as integration milestone.
```

等到 FastMCP adapter 跑通，再把 README 主标题升级为 MCP-native。

### R2. strategy 参数目前还没有形成真正 ablation

`run_eval.py` 已经支持 `--strategy`，但当前 `AgentKernel.run()` 大体按 case_type 分支执行，策略差异主要体现在 plan 文本，不足以支撑 “Agent strategies can be compared” 这个 claim。必须尽快抽出 `AgentStrategy` 接口，让 `react_agent`、`plan_execute_agent`、`guarded_agent`、`reflective_agent` 至少在工具选择、policy gate 调用时机、repair 行为或 context budget 上产生可解释差异。

### R3. toy code repair 不能继续用 stub success

当前 toy_code_repair 分支返回固定 repair_plan 且 `success=True`。这在设计期可以接受，但一旦 README 展示 sample report，会削弱可信度。建议在真实 patch/test loop 完成前，将该 case 标记为 `status=pending` 或 `success=False` + `metrics={"repair_loop_stub": true}`，避免看起来像伪造成功。

### R4. eval 容易被 reviewer 认为“太 toy”

80-120 条 case 的数量目标不错，但数量不能替代有效性。更重要的是：

- sensitive action 必须有 allow / block / review 的平衡集。
- prompt injection 和 retrieval poisoning 必须包含明确的 negative controls。
- RAG QA 不能只看 gold_doc_id 命中，还要看 citation coverage / unsupported answer / poisoned context ignore。
- workspace repair 必须至少有真实失败测试、patch diff、rerun result。

### R5. 与 Loomstead 的边界要继续压紧

Loomstead 已覆盖 trace、counterfactual replay、audit case cards。ContextGuard 不应该再变成 Agent observability 项目。这里的 trace 只服务于 eval、strategy ablation、policy decision 和 case card，不做通用观测平台。

## Missing higher-level role signals

1. **策略抽象。** 需要一个正式 `AgentStrategy` protocol / base class：`plan()`、`next_action()`、`observe()`、`reflect()`、`finalize()`。

2. **工具契约。** 需要 `ToolSpec`：`name`、`description`、`input_schema`、`output_schema`、`risk_level`、`side_effect`、`required_evidence`、`mcp_exposure`。

3. **policy gate 嵌入 ToolExecutor。** 现在 policy 是 case 分支逻辑。更理想的结构是：Agent 尝试调用 sensitive tool，ToolExecutor 先生成 PolicyDecision，再决定 allow / block / review，并把结果写入 trace。

4. **失败分类。** 增加 `failure_mode`：`wrong_doc`、`unsupported_answer`、`unsafe_allow`、`false_block`、`injection_followed`、`repair_failed`、`budget_exceeded`。

5. **ablation 解释。** 报告不能只列 leaderboard。需要说明为什么 guarded_agent 降低 unsafe_allow，为什么 reflective_agent 提升 repair_success，但带来 tool_call / latency / cost_proxy 上升。

6. **三分钟 README 证据链。** README 首页需要一张架构图、一条 CLI、一张 leaderboard、一张 case card 摘要、一个 honest boundary。

## Over-scoped parts to cut

- W1/W2 不做 A2A。
- W1/W2 不接真实开源 repo repair task。
- W1/W2 不做重 RAG pipeline、vector DB、embedding 调参。
- MVP 不做 UI。
- MVP 不做通用 guardrail rule library。
- `context_budget_agent` 可以先做简化版：限制 retrieved chunks / max tool calls / max context chars；不要做复杂优化算法。

## Recommended final scope

### Must-have

- Unified `CaseSpec` + validation。
- `AgentStrategy` interface + 至少 4 个可比较策略：react、plan_execute、guarded、reflective。
- `ToolSpec` + `ToolRegistry` + `ToolExecutor`。
- Retrieval tools：`search_docs`、`read_doc`、`verify_citation`。
- Sensitive tools：`export_data`、`delete_record`、`change_policy` mock actions，并由 policy gate 拦截。
- Trace：`TraceEvent`、`ToolCallTrace`、`PolicyDecision`、`RunRecord`。
- Metrics：success、tool_calls、evidence_coverage、unsafe_allow、false_block、repair_success、cost_proxy、latency_proxy。
- Reports：strategy ablation、guardrail eval、case cards。
- 3 张强 case card：RAG citation / sensitive action / code repair。

### Should-have

- Prompt injection + retrieval poisoning case family。
- Basic context budget strategy。
- FastMCP adapter，把已有工具暴露成 MCP-compatible server。
- CI / smoke tests / fixture validation。

### Stretch

- A2A reviewer handoff。
- Hosted LLM planner。
- Real open-source repo repair tasks。
- 更复杂的 cost-quality frontier 图表。

### Cut

- UI。
- 通用 RAG 平台。
- 企业级安全 claim。
- 全量 coding agent。
- 与公司经验相似的大型安全规则库。

## Concrete changes to docs / architecture / eval

### README

建议把首屏结构改为：

```text
1. One-liner: Agent evaluation workbench for governed tool use.
2. Why it exists: public gap in MCP-style tool boundary + agent strategy eval.
3. 3-minute demo: run eval -> generate report -> inspect case card.
4. Current status badge: Phase 1 / Phase 2, not production.
5. Evidence table: claim -> artifact link.
```

### Architecture

建议核心数据流调整为：

```text
CaseSpec
  -> AgentStrategy
  -> AgentKernel
  -> ToolExecutor
       -> InjectionCheck
       -> EvidencePolicyEngine, if sensitive / side-effectful
       -> ToolRegistry.call()
  -> TraceRecorder
  -> Evaluator
  -> Report + CaseCards
```

### Schema

建议补充：

```python
@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    risk_level: Literal["read", "write", "sensitive"]
    side_effect: bool
    required_evidence: list[str]
    mcp_exposed: bool = False

@dataclass(slots=True)
class TraceEvent:
    case_id: str
    strategy: str
    step_index: int
    event_type: Literal["plan", "tool_call", "observation", "policy_decision", "reflection", "final"]
    payload: dict[str, Any]
    latency_ms: int = 0
```

### Eval

建议把 report 从单一 success 表升级为 family-level + strategy-level：

```text
- Overall summary
- By family: RAG / injection / poisoning / sensitive / repair
- By strategy: success / safety / cost_proxy / tool_calls
- Bad-case taxonomy
- Top 3 case cards
- Claim evidence table
```

## One-month development plan

### Phase 0：Review freeze

目标：锁定项目定位和 cut list。  
交付：至少 2 份 review、项目主轴、must-have / stretch / cut、README honest wording。  
门槛：所有公开 claim 都能映射到 artifact。

### Phase 1：Contracts and deterministic baseline

目标：把项目从“可运行 starter”升级成“可扩展骨架”。  
交付：CaseSpec validation、ToolSpec、ToolExecutor、TraceEvent、multi-strategy CLI skeleton、smoke tests。  
门槛：`run_eval.py --strategies react,guarded` 能跑出按 strategy 分组的 JSONL。

### Phase 2：Policy gate and trace correctness

目标：让 evidence-gated execution 成为真实执行链路。  
交付：sensitive tool mock、PolicyDecision trace、allow/block/review cases、unsafe_allow / false_block。  
门槛：每个 sensitive action 都必须有 attempted tool call + policy decision + final outcome。

### Phase 3：Strategy ablation

目标：让策略差异可测、可解释。  
交付：react、plan_execute、guarded、reflective、简化 context_budget。  
门槛：同一批 cases 跑 4 个策略，报告展示 success / safety / cost_proxy 差异。

### Phase 4：Case expansion and eval validity

目标：让数据集质量足够支撑展示。  
交付：40-60 条高质量 cases，覆盖 RAG、injection、poisoning、sensitive action。  
门槛：至少 5 个 bad cases 被 case card 或 taxonomy 解释清楚。

### Phase 5：Workspace repair loop

目标：补齐 coding-agent-like 信号，但保持 bounded。  
交付：fixture repo generator、read_file/search_repo/apply_patch/run_tests、8-12 个真实 patch/test cases。  
门槛：每个 repair case 有 failing test、patch diff、rerun result、trace。

### Phase 6：Public packaging

目标：三分钟让 reviewer 看懂价值。  
交付：final README、sample report、3 张 case cards、resume bullets、architecture diagram。  
门槛：README 能从 claim 直接跳到 report/trace/case card。

## Suggested success definition

把原来的“一月成功定义”拆成两层：

### Portfolio MVP

- 40-60 条高质量 cases。
- 4 个真实可区分策略。
- sensitive action policy gate 完整闭环。
- 至少 8 个 workspace repair cases，真实 patch/test。
- 1 份 strategy ablation report。
- 1 份 guardrail eval report。
- 3 张 case cards。
- README 首屏清楚展示 claim -> evidence。

### Full target

- 80-120 条 cases。
- 20+ code repair tasks。
- FastMCP adapter。
- context_budget_agent 更完整。
- A2A reviewer handoff。

## Final recommendation

继续做，但要把项目最终故事压成一句话：

```text
A small reproducible agent-evaluation lab showing how different agent strategies behave when tool use is governed by evidence, trace, and budget.
```

最小惊艳点不是“用了多少协议名”，而是：同一批 cases 下，几个 agent 策略如何因为 tool boundary、evidence gate、reflection 和 context budget 产生不同结果，并且每个结果都能追溯到 trace、metrics、case card。
