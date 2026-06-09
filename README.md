# ContextGuard Agent Lab

> MCP-compatible agent strategy benchmark for governed tool use, retrieval, verification, and context budget tradeoffs.

ContextGuard Agent Lab is a small reproducible portfolio project for comparing agent control strategies under the same benchmark cases. It focuses on `AgentStrategy` design, MCP-compatible tool boundaries, context engineering, verification-before-answer, context-budget policy, and success-cost tradeoffs. Reflection is a full-target extension after the deterministic benchmark is stable.

中文定位：这是一个面向 Agent 算法 / 应用策略算法 / Agent eval / Context Engineering 岗位的公开展示项目。它不再主打 generic observability 或 audit harness，而是用统一 `CaseSpec` 比较不同 Agent 策略在检索、工具选择、验证、反思和上下文预算上的行为差异。

## Why This Project

当前作品组合已经覆盖：

- AlgoCoach-Flywheel：后训练、verifier、simulator、data flywheel、评测与推理基础设施。
- Loomstead：Agent runtime observability、trace、counterfactual replay、audit failure-analysis、case-card-first 展示。
- 公司项目经验：多 Agent 研判、大模型护栏、RAG 知识库、安全微服务与生产落地。

ContextGuard 需要补齐的公开缺口是：

- MCP-compatible tool schema / tool boundary。
- 标准化 Agent strategy ablation，而不是只展示单个运行时。
- Context budget、tool budget、verification budget 的 success-cost frontier。
- RAG / adversarial context 作为任务环境，而不是做 RAG 产品平台。
- 面向面试的 strategy leaderboard、failure taxonomy 和 ablation report。

## Core Claim

Agent tool use is a control policy. It should be evaluated under shared tasks, structured tool contracts, verification requirements, and budget constraints.

## Current Status

The repository is in pre-sprint alignment after Round 2 design review. The existing code is a deterministic starter skeleton; it should not yet be presented as a completed strategy benchmark.

## Initial Scope

### MVP Agent Strategies

- `react_agent`: direct observe-act baseline with minimal planning。
- `plan_execute_agent`: explicit plan, multi-step retrieval, then execution。
- `verify_then_answer_agent`: answer only after citation / consistency verification。
- `context_budget_agent`: choose retrieval/tool calls under context and cost budgets。

### Full-target Strategies

- `reflective_agent`: retry once after failed grader or tool observation。
- `llm_planner_agent`: optional cheap hosted/local model planner comparison after deterministic benchmark is stable。
- `guarded_agent`: kept as a small sensitive-action environment strategy, not the main project spine。

### Tool Layer

- Tool contract: `ToolSpec`, `ToolRegistry`, `ToolExecutor`。
- Tool manifest: `export_tool_manifest()` as the first MCP-compatible artifact。
- Retrieval tools: `search_docs`, `read_doc`, `verify_citation`。
- Verification tools: `check_answer_support`, `detect_injection`, `grade_final`。
- Budget tools / metadata: estimated context chars, tool cost, latency proxy。
- Sensitive tools: small mock family for bounded policy cases only。
- MCP adapter: FastMCP exposure for 2-3 core tools after in-process contracts are stable。

### Evaluation Dimensions

- Task success。
- Mean tool calls。
- Context chars / cost proxy。
- Citation coverage and unsupported answer rate。
- Verification call rate and verification benefit。
- Reflection recovery rate。
- Budget violation rate。
- Unsafe allow / false block only for the small sensitive-action family。

## Repository Layout

```text
contextguard-agent-lab/
  config/                       # Policy and pipeline configs
  data/                         # Public toy corpus and benchmark samples
  docs/                         # Design decisions and project plan
  reports/                      # Generated reports and case cards
  scripts/                      # CLI entrypoints
  src/contextguard_agent_lab/    # Agent strategies, tools, eval, trace
  tests/                        # Unit tests
```

## Design Review Workspace

- `docs/design/README.md`: design document index。
- `docs/design/03_vision_and_positioning.md`: role positioning and portfolio fit。
- `docs/design/04_architecture_skeleton.md`: architecture and module boundaries。
- `docs/design/05_claim_and_eval_contract.md`: allowed claims and required evidence。
- `docs/design/07_roadmap_and_gates.md`: phased gates。
- `docs/design/09_loomstead_overlap_and_pivot.md`: overlap audit and pivot rationale。
- `docs/design/10_execution_alignment_plan.md`: execution plan for multi-agent implementation。
- `docs/review/00_multi_model_review_packet.md`: packet for the next external / multi-model review。
- `docs/review/02_round2_synthesis.md`: accepted Round 2 execution baseline。

## Starter Smoke Workflow

This workflow checks the starter skeleton and produces a smoke report. It is not final benchmark evidence yet.

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --case-limit 3 --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
```

## Honest Boundaries

- This repo is an agent strategy benchmark and engineering pattern demo。
- It does not claim production-grade enterprise security。
- It does not implement a full Claude Code / Codex replacement。
- It does not replace Loomstead's observability / audit story。
- It uses toy public cases first; company data is excluded by design。
- `MCP-compatible` means tool contracts first; FastMCP adapter becomes claimable only after it is implemented and demonstrated。
- Public starter reports must not present `toy_code_repair` as an implemented success path before a real patch / test loop exists。
