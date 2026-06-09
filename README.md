# ContextGuard Agent Lab

> Run the same agent task across multiple control strategies, then compare tool traces, independent grading, and success-cost tradeoffs.

ContextGuard is a small MCP-compatible agent strategy benchmark. It answers one practical question:

```text
When the task, tools, and budget stay fixed, how do different agent strategies behave?
```

The current MVP strategies are `react`, `plan_execute`, `verify_then_answer`, and `context_budget`.

## What It Shows

| Capability | Current Artifact |
|---|---|
| Same cases across multiple strategies | `scripts/run_eval.py --strategies ...` |
| Structured tool boundary | `ToolSpec`, `ToolExecutor`, `reports/tool_manifest.json` |
| Independent grading | `eval/graders.py`, `grader_result` in JSONL runs |
| Cost and context accounting | `cost_proxy`, `context_chars_used`, per-call trace fields |
| Starter strategy comparison | `reports/sample_report.md` |

## 3-Minute Run

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --case-limit 3 --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
python scripts/export_tool_manifest.py --out reports/tool_manifest.json
```

The default smoke run executes 3 starter cases across 4 strategies and writes 12 run records.

## Inspect The Results

| File | What To Look For |
|---|---|
| `reports/sample_report.md` | Compact table of case, strategy, success, cost, context, and grader reason. |
| `reports/sample_run.jsonl` | Full structured run records with tool calls and independent grader output. |
| `reports/tool_manifest.json` | MCP-compatible tool contract manifest with schemas, risk, side effect, and cost metadata. |
| `data/benchmark/cases.sample.jsonl` | Starter `CaseSpec` examples with family, dimensions, budget, expected outcome, and grader spec. |

## How It Works

```text
CaseSpec
  -> AgentStrategy
  -> ToolExecutor(ToolSpec)
  -> RunRecord JSONL
  -> independent GraderResult
  -> Markdown report
```

Current strategy differences are intentionally small and deterministic:

| Strategy | Behavior |
|---|---|
| `react` | Search once, answer directly. |
| `plan_execute` | Retrieve more candidates before answering. |
| `verify_then_answer` | Search, then call `verify_citation` before final grading. |
| `context_budget` | Use conservative retrieval and verification under budget limits. |

## Current Status

Phase 1 is in progress. Implemented so far:

- `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`, and `GraderResult`.
- `ToolSpec`, `ToolRegistry`, `ToolExecutor`, and manifest export.
- `AgentStrategy` protocol and four deterministic MVP strategy skeletons.
- Independent starter graders for retrieval QA, sensitive-action smoke cases, and unimplemented coding fixtures.
- Multi-strategy CLI smoke workflow.

The project is not yet a completed benchmark. The current report is a starter smoke artifact; the next milestone is adding 8-10 strategy-difference seed cases and richer by-strategy metrics.

## Project Map

```text
contextguard-agent-lab/
  data/benchmark/              # CaseSpec JSONL samples
  data/corpus/                 # Public toy corpus
  docs/design/                 # Architecture, execution, showcase plans
  reports/                     # Generated traces, manifests, reports
  scripts/                     # CLI entrypoints
  src/contextguard_agent_lab/   # Strategies, tools, graders, traces
  tests/                       # Unit tests
```

## Design Notes

- Execution plan: `docs/design/10_execution_alignment_plan.md`
- Showcase entry plan: `docs/design/11_showcase_entry_design.md`
- Round 2 review baseline: `docs/review/02_round2_synthesis.md`
- Claim and eval contract: `docs/design/05_claim_and_eval_contract.md`

## Next Milestones

| Milestone | Output |
|---|---|
| Seed case suite | 8-10 cases designed by retrieval depth, verification timing, budget pressure, adversarial context, and tool-boundary dimensions. |
| Report upgrade | By-strategy metrics, by-family metrics, unsupported-answer rate, and budget-violation rate. |
| Budget policy upgrade | Value-of-information heuristic and success-cost frontier. |
| Showcase entry | A lightweight report index or static HTML entry that points to traces, manifests, reports, and case cards. |

## Boundaries

- Uses public toy data only.
- `MCP-compatible` currently means structured in-process tool contracts and manifest export.
- FastMCP adapter, reflective repair, LLM planner, and coding repair fixtures are later targets.
- The project avoids heavy UI; the display layer should stay lightweight and artifact-driven.
