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

## Phase 1: Contracts and Strategy Skeleton

Goal: turn the starter code from case router into strategy benchmark skeleton.

Deliverables:

- `AgentStrategy` interface。
- `ToolSpec`, `ToolRegistry`, `ToolExecutor`。
- independent grader skeleton。
- multi-strategy CLI。
- 8-10 seed cases across retrieval QA, verification-needed, budget pressure。

Gate:

```text
[ ] python -m unittest discover -s tests
[ ] Same case runs across at least 3 strategies
[ ] Tool sequences differ across strategies
[ ] Grader is not embedded in AgentKernel branch logic
```

## Phase 2: Retrieval, Verification, and Failure Cases

Goal: create non-trivial strategy differences.

Deliverables:

- retrieval tools: `search_docs`, `read_doc`, `verify_citation`。
- verification tools: `check_answer_support`, `grade_final`。
- adversarial context cases with negative controls。
- failure taxonomy starter。

Gate:

```text
[ ] At least 20 cases total
[ ] 20-30% cases fail under at least one strategy
[ ] unsupported_answer_rate differs between react and verify_then_answer
[ ] sample report includes by-family metrics
```

## Phase 3: Context Budget and Ablation Report

Goal: make cost-aware strategy tradeoffs visible.

Deliverables:

- `context_budget_agent`。
- budget specs per case。
- strategy leaderboard。
- context budget frontier report。
- top 3 case cards。

Gate:

```text
[ ] At least 4 strategies compared
[ ] report shows success / tool calls / context chars / cost proxy
[ ] budget strategy has lower cost on some cases and documented failure modes
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

Gate:

```text
[ ] Expansion strengthens strategy ablation rather than replacing it
[ ] No duplicate Loomstead observability / audit main story
[ ] New claims mapped to artifacts
```
