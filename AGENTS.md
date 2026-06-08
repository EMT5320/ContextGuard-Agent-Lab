# AGENTS.md — ContextGuard Agent Lab

## 项目定位

ContextGuard Agent Lab 是一个 MCP-native、evidence-governed 的 Agent 评测工作台，用于展示：

- Agent kernel：plan / act / observe / reflect / repair。
- MCP tool boundary：retrieval、workspace、sensitive action 工具通过统一 registry 暴露。
- Evidence-gated tool execution：高风险动作必须满足 evidence contract。
- Agent eval：任务成功率、工具调用效率、修复成功率、安全指标、成本与延迟。

## 协作原则

- 文档优先使用简体中文，面向公开 README 的关键术语可保留英文。
- 代码注释默认使用英文，便于开源展示；新增代码要保留必要注释，解释边界和安全假设。
- 不引入公司数据、内部接口、内部安全策略或私密路径。
- 不声明企业级安全能力，只声明 bounded benchmark 与 engineering pattern。
- 任何新增功能都应进入至少一个 report、trace、metric 或 case card。
- UI 暂不进入主线，优先 CLI、JSONL trace、Markdown report。

## 默认验证

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --case-limit 3 --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
```
