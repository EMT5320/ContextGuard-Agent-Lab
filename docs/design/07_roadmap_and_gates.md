# Roadmap and Gates

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
[ ] At least one new review collected against the revised strategy-benchmark scope.
[ ] Project positioning decided: MCP-compatible Agent Strategy Benchmark.
[ ] Must-have / should-have / stretch / cut list confirmed.
[ ] README wording aligned with allowed claims.
```

## Phase 0.5: Pre-sprint Alignment

Goal: align code metadata and public starter artifacts with the revised scope before deeper implementation.

Deliverables:

- `pyproject.toml` description updated away from old `MCP-native / evidence-governed` wording。
- default report renamed or regenerated as starter smoke report。
- `toy_code_repair` stub removed from default quickstart or marked `stub_not_claimed` / unsuccessful。
- MVP strategy set consistently documented as `react`, `plan_execute`, `verify_then_answer`, `context_budget`。
- simple `cost_proxy` formula documented。

Gate:

```text
[ ] No public default artifact shows repair stub success
[ ] Package metadata matches README positioning
[ ] Quickstart output is labeled smoke / starter, not final benchmark evidence
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

Gate:

```text
[ ] At least 20 cases total
[ ] 20-30% cases fail under at least one strategy
[ ] unsupported_answer_rate differs between react and verify_then_answer
[ ] at least 5 cases declare their intended strategy-difference dimension
[ ] sample report includes by-family metrics
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
