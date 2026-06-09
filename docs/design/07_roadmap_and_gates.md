# Roadmap and Gates

This roadmap is an execution contract, not a list of independent demos. A phase is not done until its artifacts flow into trace, metric, report, or case-card evidence and preserve the same-case / multi-strategy benchmark loop.

## Phase 0: Pivot Review Gate

Goal: lock the revised project vision before heavy implementation.

Deliverables:

- updated README and design docs。
- Loomstead overlap / pivot note。
- claim/eval contract。
- risk register and cut line。
- updated multi-model review packet。

Gate:

```text
[x] At least one new review collected against the revised strategy-benchmark scope.
[x] Project positioning decided: MCP-compatible Agent Strategy Benchmark.
[x] Must-have / should-have / stretch / cut list confirmed.
[x] README wording aligned with allowed claims.
```

Decision source: `docs/review/02_round2_synthesis.md`.

## Phase 0.5: Pre-sprint Alignment

Goal: align code metadata and public starter artifacts with the revised scope before deeper implementation.

Deliverables:

- `pyproject.toml` description updated away from old `MCP-native / evidence-governed` wording。
- default report renamed or regenerated as starter smoke report。
- `toy_code_repair` stub removed from default quickstart or marked `stub_not_claimed` / unsuccessful。
- MVP strategy set consistently documented as `react`, `plan_execute`, `verify_then_answer`, `context_budget`。
- simple `cost_proxy` formula documented。
- multi-agent execution plan added as `docs/design/10_execution_alignment_plan.md`。

Gate:

```text
[x] No public default artifact shows repair stub success
[x] Package metadata matches README positioning
[x] Quickstart output is labeled smoke / starter, not final benchmark evidence
[x] Future-agent instructions point to the execution alignment plan
```

## Phase 1: Contracts and Strategy Skeleton

Goal: turn the starter code from case router into strategy benchmark skeleton.

Deliverables:

- `AgentStrategy` interface。
- `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`。
- `ToolSpec`, `ToolRegistry`, `ToolExecutor`。
- `export_tool_manifest()`。
- independent grader skeleton。
- multi-strategy CLI。
- 8-10 seed cases across retrieval QA, verification-needed, budget pressure。

Parallel lanes:

- Benchmark contracts agent: `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`, loader validation。
- Tool boundary agent: `ToolSpec`, `ToolExecutor`, manifest export, retrieval tool wrapping。
- Strategy agent: `AgentStrategy` protocol and first three deterministic strategy classes。
- Eval agent: independent grader skeleton and RunRecord grader fields。

Gate:

```text
[ ] python -m unittest discover -s tests
[ ] Same case runs across at least 3 strategies
[ ] Tool sequences differ across strategies
[ ] Grader is not embedded in AgentKernel branch logic
[ ] Tool manifest exposes name / schema / risk / cost / mcp exposure metadata
```

## Phase 2: Retrieval, Verification, and Failure Cases

Goal: create non-trivial strategy differences.

Deliverables:

- retrieval tools: `search_docs`, `read_doc`, `verify_citation`。
- verification tools: `check_answer_support`, `grade_final`。
- adversarial context cases with negative controls。
- cases authored by strategy-difference dimensions。
- failure taxonomy starter。

Parallel lanes:

- Case authoring agent: dimension-led cases and negative controls。
- Tool agent: verification tool payloads and structured errors。
- Eval/report agent: by-family metrics and unsupported-answer metrics。

Gate:

```text
[ ] At least 20 cases total
[ ] 20-30% cases fail under at least one strategy
[ ] unsupported_answer_rate differs between react and verify_then_answer
[ ] at least 5 cases declare their intended strategy-difference dimension
[ ] sample report includes by-family metrics
```

## Phase 2.5: Showcase Entry Upgrade

Goal: make the project understandable before the final public packaging phase.

Deliverables:

- README kept as a concise landing page。
- `reports/README.md` updated as artifact index。
- first case card or report excerpt showing a real strategy split。
- optional static showcase decision recorded after Phase 3 report quality is known。

Gate:

```text
[ ] README explains what runs, what is compared, and where artifacts are in 3 minutes
[ ] Report index links generated traces, reports, manifests, and planned case cards
[ ] Showcase layer reuses existing artifacts instead of creating a separate product UI
```

## Phase 3: Context Budget and Ablation Report

Goal: make cost-aware strategy tradeoffs visible.

Deliverables:

- `context_budget_agent`。
- value-of-information budget heuristic。
- budget specs per case。
- strategy leaderboard。
- context budget frontier report。
- Pareto / dominated strategy analysis。
- top 3 case cards。

Parallel lanes:

- Strategy agent: VoI-based `context_budget_agent`。
- Eval agent: cost proxy, success-conditioned cost, Pareto / dominated analysis。
- Report agent: ablation report and context budget frontier。

Gate:

```text
[ ] At least 4 strategies compared
[ ] report shows success / tool calls / context chars / cost proxy
[ ] budget strategy has lower cost on some cases and documented failure modes
[ ] report explains why context budget policy works or fails
[ ] at least 3 bad cases explained
```

## Phase 4: MCP Adapter and Public Packaging

Goal: convert tool boundary into a visible protocol story.

Deliverables:

- FastMCP adapter for 2-3 core tools。
- final README evidence table。
- architecture diagram。
- resume bullets。
- optional static showcase page if Markdown artifacts are no longer enough。

FastMCP remains optional until the in-process `ToolSpec` / `ToolExecutor` boundary is stable. If it is not implemented, README must keep `MCP-compatible` wording and avoid `MCP-native` claims。

Gate:

```text
[ ] CLI workflow documented
[ ] reports link to traces
[ ] FastMCP adapter either demonstrated or README wording remains MCP-compatible only
[ ] public story fits allowed claims
```

## Phase 5: Optional Expansion

Goal: add secondary task environments only after strategy benchmark is strong.

Candidate deliverables:

- small sensitive-action balanced set。
- 3-5 bounded coding fixture cases。
- reflective repair loop with real test rerun。
- hosted LLM planner comparison。
- MCP tool-boundary adversarial cases beyond MVP smoke。

Gate:

```text
[ ] Expansion strengthens strategy ablation rather than replacing it
[ ] No duplicate Loomstead observability / audit main story
[ ] New claims mapped to artifacts
```
