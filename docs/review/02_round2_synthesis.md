# Round 2 Review Synthesis

> Date: 2026-06-09
> Inputs: `docs/review/reviews/round2/5.5pro.md`, `docs/review/reviews/round2/opus4.8.md`, `docs/review/reviews/round2/GLM.md`
> Status: accepted synthesis after follow-up battle; model reviewers raised no objections to the final consolidation.

## 1. Final Round 2 Verdict

Continue ContextGuard, but keep the revised project spine narrow:

```text
MCP-compatible Agent Strategy Benchmark
  -> Cost-aware Agent Control Policy
  -> optional MCP-governed / LLM-backed expansion
```

The MVP should not expand into another Loomstead-style observability / audit project, and it should not start with hosted LLM planning. The first implementation sprint must make the benchmark spine real: same cases, different strategies, structured tools, independent grading, and ablation reports.

## 2. Consensus Across Models

All round2 reviews agree on these points:

- The pivot away from `evidence-governed workbench` is correct.
- The project now has a valid portfolio gap: AgentStrategy ablation, MCP-compatible tool boundary, context budget, verification tradeoffs.
- Current code still lags behind docs: kernel is a `case_type` router, strategy is a label, success grading is inside kernel, repair stub reports success, and MCP compatibility lacks concrete schema evidence.
- `ToolSpec`, `ToolExecutor`, `AgentStrategy`, `BudgetSpec`, and independent grader are non-negotiable P1 items.
- Public default reports must not show `toy_code_repair` as a successful implemented capability.

## 3. Accepted Suggestions By Source

| Source | Accepted Suggestions | Decision |
|---|---|---|
| 5.5pro | Pre-sprint public-claim alignment; `BudgetSpec`; `ToolSpec`; tool manifest export; independent grader; MVP 4 strategies; reflective as Full target | Accept directly. Use as implementation order. |
| opus4.8 | Be honest about Agent algorithm signal; ContextGuard alone is strongest for eval / context engineering / application strategy; reserve learned policy as possible upgrade | Accept with framing. MVP remains deterministic; algorithm signal comes from cost-aware control policy first. |
| GLM | Design cases by strategy-difference dimensions; upgrade `context_budget_agent` to value-of-information policy; add small MCP boundary attack cases; LLM-backed strategy only after deterministic spine | Strongly accept case design and VoI policy. Defer LLM-backed strategy. |

## 4. Battle Resolutions

### 4.1 LLM-backed Strategy

Decision: not an MVP gate.

Reason: hosted LLM strategies improve realism, but they introduce non-determinism, provider config, and eval validity issues. Deterministic strategies should first prove the benchmark loop.

Accepted future path:

- Phase 4 / Full target: one cheap LLM-backed planner can compare against deterministic strategies.
- It must be reported as an optional realism experiment, not the core MVP claim.

### 4.2 Agent Algorithm Signal

Decision: do not equate Agent algorithm only with Agentic RL.

Reason: context engineering, tool routing, verification timing, and budget allocation are valid application-strategy algorithm signals. ContextGuard should make this explicit through cost-aware control policies and success-cost frontier reports.

Accepted future path:

- MVP: deterministic strategy benchmark.
- Core upgrade: `context_budget_agent` becomes a value-of-information policy.
- Optional integration: AlgoCoach can later provide learning / RL / verifier-backed policy improvement.

### 4.3 MCP Safety / Tool Boundary Cases

Decision: include small adversarial tool-boundary cases, but do not revive the old safety/audit spine.

Reason: the point is to evaluate strategy behavior at the tool boundary, not to claim enterprise MCP safety.

Accepted scope:

- 2-3 cases where poisoned context or distractor instructions try to trigger an inappropriate tool.
- Metrics remain strategy-oriented: unsupported answer, wrong tool, budget violation, unsafe allow only within the small sensitive family.

## 5. Final Scope After Round 2

### MVP

- 4 strategies: `react`, `plan_execute`, `verify_then_answer`, `context_budget`.
- `AgentStrategy` interface.
- `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`.
- `ToolSpec`, `ToolRegistry`, `ToolExecutor`.
- `export_tool_manifest()` as the first MCP-compatible artifact.
- Independent grader and by-strategy / by-family metrics.
- 10-15 seed cases first, then 20-30 MVP cases.
- Cases designed by strategy-difference dimensions.
- Starter ablation report with success-cost frontier.

### Full Target

- `reflective_agent` retry / repair.
- 2-3 core tools exposed through FastMCP.
- Optional cheap LLM-backed planner comparison.
- Small sensitive-action balanced family.
- 3-5 bounded coding fixture cases only if they strengthen strategy ablation.

### Cut

- A2A.
- Heavy UI.
- Generic RAG platform.
- Full coding agent.
- Large guardrail SDK.
- Enterprise security claims.

## 6. Implementation Order

1. Pre-sprint public-claim alignment: update package metadata, smoke report wording, and repair stub exposure.
2. Schema contracts: add `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`, `ToolSpec`.
3. Tool boundary: implement `ToolExecutor`, per-call cost/context accounting, and manifest export.
4. Strategy interface: implement 4 MVP strategies and multi-strategy CLI.
5. Independent grader: move success scoring out of kernel.
6. Seed cases: add 10-15 cases by strategy-difference dimensions.
7. First report: generate by-strategy metrics, by-family metrics, and a small success-cost frontier.
8. Upgrade `context_budget_agent`: add value-of-information scoring and Pareto analysis.

## 7. Case Design Dimensions

| Dimension | Case Design Principle | Expected Strategy Split |
|---|---|---|
| Retrieval depth | Gold evidence requires 2+ retrieval/read steps | `plan_execute` beats `react`. |
| Verification timing | Unsupported answer is plausible without citation check | `verify_then_answer` beats `react`. |
| Budget pressure | Context window cannot include all retrieved chunks | `context_budget` saves cost but may miss evidence. |
| Adversarial context | Poisoned/distractor doc conflicts with reliable evidence | Verification/budget policies resist distractor better. |
| Tool boundary | Distractor tries to trigger inappropriate tool | Tool-aware strategies avoid wrong / unsafe tool calls. |

## 8. Value-of-Information Budget Policy

MVP heuristic:

```text
chunk_value = query_relevance * source_reliability * novelty
chunk_cost = estimated_context_chars + tool_cost
selection_score = chunk_value / max(chunk_cost, 1)
```

The budget agent should choose retrieval depth, read depth, and verification calls under `BudgetSpec`. The report should explain why it works or fails, including dominated strategies and cases where lower cost causes missed evidence.

## 9. Mapping Back To Claims

- `Agent strategies can be compared under unified tasks`: requires different tool sequences and metrics across the four MVP strategies.
- `Tool use is exposed through an MCP-compatible boundary`: requires `ToolSpec` and exported manifest before FastMCP.
- `Context budget tradeoffs are measurable`: requires `BudgetSpec`, VoI policy, cost metrics, and frontier report.
- `Verification can reduce unsupported answers`: requires verification-needed cases and independent grader.
- Sensitive-action claims remain bounded and secondary.
