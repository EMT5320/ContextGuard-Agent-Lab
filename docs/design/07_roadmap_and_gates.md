# Roadmap and Gates

## Phase 0: Design review gate

Goal: lock project vision before heavy implementation.

Deliverables:

- design docs index。
- architecture skeleton。
- claim/eval contract。
- risk register。
- multi-model review packet。

Gate:

```text
[ ] At least two independent reviews collected.
[ ] Project positioning decided.
[ ] Must-have / cut-first list confirmed.
[ ] README wording aligned with allowed claims.
```

## Phase 1: Deterministic agent baseline

Deliverables:

- CaseSpec validation。
- deterministic `react_agent` and `guarded_agent`。
- retrieval and sensitive-action sample cases。
- sample report。

Gate:

```text
[ ] python -m unittest discover -s tests
[ ] sample run JSONL and report generated
[ ] all tool calls are traceable
```

## Phase 2: Strategy ablation

Deliverables:

- `plan_execute_agent`。
- `reflective_agent`。
- starter `context_budget_agent`。
- shared leaderboard。

Gate:

```text
[ ] Same cases run across 4 strategies
[ ] report shows success / tool count / cost proxy
[ ] at least 3 bad cases documented
```

## Phase 3: Workspace repair loop

Deliverables:

- bounded toy fixture generator。
- `apply_patch` and `run_tests` tools。
- 20+ toy code repair cases。
- repair success report。

Gate:

```text
[ ] fixture tasks pass from clean checkout
[ ] failed attempts are traceable
[ ] repair loop has clear limitations
```

## Phase 4: MCP and case cards

Deliverables:

- FastMCP adapter for retrieval/workspace tools。
- case cards for RAG, guardrail, code repair。
- final README and resume bullets。

Gate:

```text
[ ] CLI workflow documented
[ ] reports link to traces
[ ] public story fits allowed claims
```
