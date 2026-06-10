# AGENTS.md — ContextGuard Agent Lab

## 项目定位

ContextGuard Agent Lab 是一个 MCP-compatible、strategy-evaluation-first 的 Agent 评测工作台。当前执行基准以 `docs/review/02_round2_synthesis.md` 和 `docs/design/10_execution_alignment_plan.md` 为准，用于展示：

- Agent strategy benchmark：MVP 只包含 react / plan-execute / verify-then-answer / context-budget；reflective 属于 Full target。
- MCP-compatible tool boundary：retrieval、verification、workspace、sensitive action 工具通过统一 `ToolSpec` / registry / executor 暴露。
- Context and budget governance：检索量、上下文长度、验证次数、工具成本和成功率一起评测。
- Agent eval：任务成功率、工具调用效率、验证收益、修复/反思收益、安全指标、成本与延迟。

项目不再以 generic observability、audit harness 或 evidence-gated execution 作为主轴；这些能力已主要由 Loomstead 负责展示。ContextGuard 的主轴是策略差异、协议边界和 success-cost tradeoff。

## 协作原则

- 文档优先使用简体中文，面向公开 README 的关键术语可保留英文。
- 代码注释默认使用英文，便于开源展示；新增代码要保留必要注释，解释边界和安全假设。
- 不引入公司数据、内部接口、内部安全策略或私密路径。
- 不声明企业级安全能力，只声明 bounded benchmark 与 engineering pattern。
- 任何新增功能都应进入至少一个 report、trace、metric 或 case card。
- 重 UI 暂不进入主线；README、reports index、CLI、JSONL trace、Markdown report 是必须维护的展示入口。
- 后续多 agent 并行开发时，先对齐 `10_execution_alignment_plan.md` 的工作流分工；不要把阶段目标坍缩成互不关联的小 demo。
- `toy_code_repair`、reflective repair、LLM planner、FastMCP adapter 都不是 MVP blocker；除非已有 trace / grader / report 证据，否则不要把它们写成已实现主张。

## Label Visibility Contract

- Grader 和报告可以读取 `gold_doc_ids`、`expected_outcome`、`grader`、`metadata.intended_split`、`family` 和 dimensions。
- `AgentStrategy` 只能接收去敏的 `CaseView`，不得读取 gold label、expected outcome、intended split 或 case-family 评测标签。
- 工具实现不得接收 `expected_doc_ids` 等 gold label；verification 工具只能根据 answer、retrieved chunks、answer source ids 和运行时 provenance 判断 grounding / source support。
- `retrieval_doc_ids` 是每个 case 的运行时语料候选池，可以由 kernel 传给 retrieval 工具，但不得暴露给 `AgentStrategy`。
- `budget`、`user_query`、retrieved chunks、`source` / `trust_tier` 等运行时可见元数据可以被策略和工具使用。
- 如果新增策略或工具需要更多字段，先判断该字段是运行时环境信息还是评测真值；不确定时先写入设计文档再实现。

## 默认验证

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --case-limit 3 --strategies react,plan_execute,verify_then_answer,context_budget --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
python scripts/export_tool_manifest.py --out reports/tool_manifest.json
```

默认报告是 starter smoke artifact，不是正式 strategy benchmark 证据。
