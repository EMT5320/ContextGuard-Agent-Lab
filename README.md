# ContextGuard Agent Lab

> Run the same agent task across multiple control strategies, then compare tool traces, independent grading, and success-cost tradeoffs.

ContextGuard is a small MCP-compatible agent strategy benchmark. It answers one practical question:

```text
When the task, tools, and budget stay fixed, how do different agent strategies behave?
```

The current MVP strategies are `react`, `plan_execute`, `verify_then_answer`, and `context_budget`. An optional `llm_planner` strategy compares cheap planner output against deterministic planning.

## What It Shows

| Capability | Current Artifact |
|---|---|
| Same cases across multiple strategies | `scripts/run_eval.py --strategies ...` |
| Structured tool boundary | `ToolSpec`, `ToolExecutor`, `reports/tool_manifest.json` |
| FastMCP-demonstrated retrieval tools | `src/contextguard_agent_lab/mcp_server/server.py`, `scripts/smoke_fastmcp.py` |
| Independent grading | `eval/graders.py`, `answer_source_doc_ids`, `grader_result` in JSONL runs |
| Cost and context accounting | `cost_proxy`, `context_chars_used`, per-call trace fields |
| Deterministic vs cheap-planner comparison | `reports/planner_comparison.md`, `reports/planner_comparison.jsonl` |
| Seed strategy comparison | `reports/sample_report.md`, `reports/agent_strategy_ablation.md` |

## Claim-Evidence Map

| Claim | Evidence Artifact |
|---|---|
| Same cases compare multiple deterministic agent strategies. | `reports/agent_strategy_ablation.md`, `reports/agent_strategy_ablation.jsonl` |
| Tool use is exposed through an MCP-compatible in-process boundary. | `reports/tool_manifest.json`, `src/contextguard_agent_lab/tools/registry.py` |
| Two core tools are demonstrated through FastMCP. | `scripts/smoke_fastmcp.py`, `mcp_server/server.py`, `mcp_exposure=fastmcp` rows in `reports/tool_manifest.json` |
| Independent grading is stored separately from agent answers. | `grader_result` fields in `reports/agent_strategy_ablation.jsonl` |
| Strategies and tools do not receive gold labels. | `CaseView`, gold-free `verify_citation` traces, `docs/design/05_claim_and_eval_contract.md` |
| Context and budget tradeoffs are measurable. | `reports/context_budget_frontier.md`, `reports/agent_strategy_ablation.md` |
| Representative strategy splits are inspectable. | `reports/case_cards.md` |
| Cheap planner behavior is compared against deterministic planning. | `reports/planner_comparison.md` |

## 3-Minute Run

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --case-limit 3 --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
python scripts/export_tool_manifest.py --out reports/tool_manifest.json
```

The default smoke run executes 3 starter cases across 4 strategies and writes 12 run records.

Generate the fuller seed-suite ablation:

```powershell
python scripts/run_eval.py --strategies react,plan_execute,verify_then_answer,context_budget --out reports/agent_strategy_ablation.jsonl
python scripts/generate_report.py --run reports/agent_strategy_ablation.jsonl --out reports/agent_strategy_ablation.md
```

### FastMCP Demo

Install the optional MCP extra, then smoke-test the two demonstrated tools in-process:

```powershell
pip install -e ".[mcp]"
python scripts/smoke_fastmcp.py --query "MCP retrieval tool"
```

Expected output includes `search_docs` and `verify_citation` in the `tools` list plus `verify_supported: true` on the starter query.

To run the stdio server directly:

```powershell
python -m contextguard_agent_lab.mcp_server.server
```

### Planner Comparison

Compare deterministic `plan_execute` against offline cheap keyword planner `llm_planner` on rag cases:

```powershell
python scripts/run_planner_comparison.py
```

Current seed-suite headline (`reports/planner_comparison.md`, 7 rag cases):

| Strategy | Success | Missing verification | Mean cost |
|---|---:|---:|---:|
| `plan_execute` | 71.4% | 14.3% | 1.622 |
| `llm_planner` | 71.4% | 0.0% | 1.776 |

Interpretation: the cheap planner trades higher cost (+0.155 mean cost proxy) for fixing the verification-needed failure mode, but still misses the adversarial shallow-retrieval split that deterministic `plan_execute` passes. Default backend is offline keyword policy (`data/planner/cheap_planner_policy.json`); hosted OpenAI-compatible planning is optional via `CONTEXTGUARD_PLANNER_BACKEND=http`.

## Inspect The Results

| File | What To Look For |
|---|---|
| `reports/sample_report.md` | Compact smoke report with aggregate metrics and run detail. |
| `reports/agent_strategy_ablation.md` | Seed-suite by-strategy / by-family metrics, observed splits, and success-cost view. |
| `reports/planner_comparison.md` | Deterministic vs cheap-planner headline metrics on rag cases. |
| `reports/sample_run.jsonl` | Full structured run records with tool calls and independent grader output. |
| `reports/agent_strategy_ablation.jsonl` | Full seed-suite run records across the four MVP strategies. |
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
| `llm_planner` | Optional cheap planner decides retrieval depth and verification timing. |

## Current Status

Phase 1 freeze snapshot (2026-06-11):

- `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`, and `GraderResult`.
- `ToolSpec`, `ToolRegistry`, `ToolExecutor`, and manifest export.
- `AgentStrategy` protocol and four deterministic MVP strategy skeletons using label-free `CaseView`.
- FastMCP demonstration for `search_docs` and `verify_citation`.
- Cheap offline planner comparison against `plan_execute`.
- Independent starter graders for retrieval QA, sensitive-action smoke cases, and unimplemented coding fixtures.
- Answer-source tracing, abstention tracing, and gold-free verification over retrieved chunks and runtime provenance.
- Per-case retrieval doc pools for stable seed-case retrieval as the toy corpus grows.
- Context-budget selection reasons using query relevance, source reliability, novelty, and estimated context cost.
- 11 public starter cases covering retrieval depth, verification timing, budget pressure, adversarial context, source reliability, simulated `export_data` tool-boundary paths, and a clearly marked coding stub.
- Multi-strategy CLI smoke and seed-suite report workflow with coding fixtures excluded from core aggregates.

The project is a bounded benchmark, not a production agent platform. The ablation report is seed-suite evidence for strategy comparison and eval-validity discipline.

## Project Map

```text
contextguard-agent-lab/
  data/benchmark/              # CaseSpec JSONL samples
  data/corpus/                 # Public toy corpus
  data/planner/                # Offline cheap planner policy
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

## Boundaries (Frozen)

| Topic | Status |
|---|---|
| Data | Public toy corpus only; no company or private data. |
| MCP claim | `MCP-compatible` = in-process `ToolSpec` + manifest export. `FastMCP demonstrated` applies only to `search_docs` and `verify_citation`. `export_data` remains manifest-only. |
| Strategies | MVP = four deterministic strategies. `llm_planner` is an optional comparison strategy with offline keyword backend by default, not a frontier-model claim. |
| Grading | Graders read gold labels; strategies and tools do not. |
| Coding repair | `cg_code_001` is a stub excluded from core aggregate metrics. |
| Not claimed | Enterprise security, MCP-native for all tools, reflective repair, hosted frontier LLM planning, production observability. |
| UI | Artifact-driven README / JSONL / Markdown only; no heavy UI in scope. |
