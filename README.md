# ContextGuard Agent Lab

> MCP-native, evidence-governed agent evaluation workbench.

ContextGuard Agent Lab is a small but complete portfolio project for evaluating agent systems under unified cases. It focuses on agent kernel design, MCP-style tool boundaries, evidence-gated tool execution, traceability, and reproducible evaluation.

中文定位：这是一个面向 Agent 算法 / 大模型应用 / Agent 工程岗位的公开展示项目。它把检索、工作区操作和敏感动作抽象成统一工具，由 agent 在同一批 CaseSpec 上执行任务，并输出 trace、policy decision、metrics 与 case report。

## Why this project

当前项目组合已经覆盖：

- AlgoCoach-Flywheel：后训练、verifier、simulator、data flywheel、评测与推理基础设施。
- Loomstead：Agent runtime observability、trace、counterfactual replay、audit failure analysis。
- 公司项目经验：多 Agent 研判、大模型护栏、RAG 知识库、安全微服务与生产落地。

ContextGuard Agent Lab 补齐公开展示中的高频缺口：

- MCP / standard tool protocol boundary。
- Agent planning / acting / reflection / repair loop。
- RAG + Agent 融合的策略与成本评测。
- Evidence-gated sensitive tool execution。
- Coding-agent-like workspace task execution 的最小闭环。

## Core claim

Context is not just retrieved; it is governed, traced, and evaluated.

## Initial scope

### Agent strategies

- `react_agent`: simple observe-and-act loop。
- `plan_execute_agent`: explicit plan then tool execution。
- `reflective_agent`: retry after failed observation。
- `guarded_agent`: policy gate before sensitive action。
- `context_budget_agent`: placeholder for context-cost tradeoff experiments。

### Tool layer

- Retrieval tools: `search_docs`, `read_doc`, `verify_citation`。
- Workspace tools: `list_files`, `read_file`, `search_repo`, `apply_patch`, `run_tests`。
- Sensitive tools: `export_data`, `delete_record`, `change_policy` as mock policy-gated actions。

### Evaluation dimensions

- Task success。
- Tool-call efficiency。
- Repair success。
- Evidence coverage。
- Unsafe allow rate。
- False block rate。
- Latency and approximate token/cost proxy。

## Repository layout

```text
contextguard-agent-lab/
  config/                       # Policy and pipeline configs
  data/                         # Public toy corpus and benchmark samples
  docs/                         # Design decisions and project plan
  reports/                      # Generated reports and case cards
  scripts/                      # CLI entrypoints
  src/contextguard_agent_lab/    # Agent kernel, tools, guardrails, eval, trace
  tests/                        # Unit tests
```


## Design review workspace

The project is currently in a design-review phase before heavy implementation:

- `docs/design/README.md`: design document index.
- `docs/design/03_vision_and_positioning.md`: role positioning and portfolio fit.
- `docs/design/04_architecture_skeleton.md`: architecture and module boundaries.
- `docs/design/05_claim_and_eval_contract.md`: allowed claims and required evidence.
- `docs/design/06_risk_register.md`: scope and failure-mode risks.
- `docs/design/07_roadmap_and_gates.md`: phased gates.
- `docs/design/08_background_snapshot.md`: sanitized background, portfolio fit, and target-role update.
- `docs/review/00_multi_model_review_packet.md`: packet for external / multi-model review.
## Quick start

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --case-limit 3 --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
```

## Honest boundaries

- This repo is an evaluation workbench and engineering pattern demo.
- It does not claim production-grade enterprise security.
- It does not implement a full Claude Code / Codex replacement.
- It uses toy public cases first; real company data is excluded by design.
- A2A is reserved as a thin reviewer handoff stretch goal.



