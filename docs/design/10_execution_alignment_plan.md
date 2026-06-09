# Execution Alignment Plan

> Status: accepted planning baseline after Round 2 synthesis.
> Source of truth: `docs/review/02_round2_synthesis.md` first, then `README.md`, `AGENTS.md`, and this document.
> Purpose: keep future multi-agent implementation aligned around one benchmark spine instead of drifting into isolated demos.

## 1. Project Spine Lock

ContextGuard Agent Lab must progress through this spine:

```text
same CaseSpec
  -> different AgentStrategy implementations
  -> structured ToolSpec / ToolExecutor calls
  -> independent grading
  -> by-strategy and by-family metrics
  -> success-cost frontier and case cards
```

The project is not complete because any one phase can run a small scenario. It is complete only when the same benchmark loop produces comparable traces, metrics, and reports across strategies.

## 2. Scope Decisions

| Area | Decision | Rationale |
|---|---|---|
| MVP strategies | `react`, `plan_execute`, `verify_then_answer`, `context_budget` | These create retrieval-depth, verification-timing, and budget-allocation splits. |
| Full-target strategies | `reflective`, optional `llm_planner`, small `guarded` sensitive-family strategy | Useful after deterministic benchmark validity is stable. |
| MCP claim | `MCP-compatible` via `ToolSpec`, registry, executor, trace, manifest | FastMCP adapter is a Full target artifact, not an MVP blocker. |
| Algorithm signal | Cost-aware control policy and VoI budget heuristic first | Stronger than label-only deterministic branches and still reproducible. |
| Sensitive action | 1-2 MVP smoke / tool-boundary cases at most | Supports boundary evaluation without reviving the old audit spine. |
| Coding fixture | Excluded from MVP quickstart | Only add if reflective repair strengthens strategy ablation. |
| Showcase layer | Lightweight landing, report index, and optional static page | Heavy app UI is cut, but reviewer-facing entry quality is required from Phase 1. |

## 3. Current Alignment Gaps

| Gap | Current Symptom | Blocking Risk | Target Resolution |
|---|---|---|---|
| Strategy is too shallow | `AgentStrategy` exists, but current strategies only vary retrieval depth and verification timing | Ablation can remain thin | Expand cases and strategy actions before claiming benchmark results. |
| Grading is starter-only | `eval/graders.py` exists for starter families | Eval validity can be overstated | Add family-specific graders and negative controls. |
| Tool boundary is partial | `ToolSpec` / `ToolExecutor` exist for starter retrieval and verification tools | MCP-compatible evidence remains narrow | Add read / verify / tool-boundary tools and manifest coverage. |
| Budget signal is partial | `BudgetSpec` and per-call accounting exist | `context_budget_agent` can still become throttling | Add explicit VoI scoring and budget-pressure cases. |
| Report is smoke-only | Starter report is not strategy ablation | Public claims can overreach | Keep smoke wording until by-strategy report exists. |
| Cases are not dimension-led yet | Starter cases are task-type examples | Strategies may not separate | Author cases by strategy-difference dimensions. |

## 4. Workstreams For Parallel Agents

Parallel agents should own one workstream at a time and avoid changing another workstream's files unless the task explicitly requires it.

| Workstream | Main Files | Owns | Must Not Own |
|---|---|---|---|
| Benchmark Contracts | `src/.../benchmark/`, `data/benchmark/`, schema tests | `CaseSpec`, `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`, case validation | Strategy control logic. |
| Tool Boundary | `src/.../tools/`, `src/.../mcp_server/`, tool tests | `ToolSpec`, `ToolRegistry`, `ToolExecutor`, manifest, retrieval and verification tools | Grader success policy except tool-observation payloads. |
| Strategy Kernel | `src/.../agents/`, agent tests | `AgentStrategy`, kernel loop, four MVP strategies, strategy action traces | Final success scoring. |
| Eval And Reports | `src/.../eval/`, `scripts/generate_report.py`, `reports/` | independent graders, metrics, frontier, case cards, Markdown reports | Tool implementation details. |
| Showcase And Packaging | `README.md`, `reports/README.md`, `docs/design/`, `docs/review/`, resume bullets | landing page, artifact index, claim-evidence mapping, public story | Core implementation behavior without tests. |

Handoff rule: each agent should report changed files, commands run, new artifacts generated, and any claim that still lacks evidence.

## 5. Phase Plan

### Phase 0.5: Alignment Landing

Goal: ensure public metadata, default reports, and contributor instructions no longer contradict Round 2.

Implementation content:

- Replace old `MCP-native / evidence-governed` metadata with MCP-compatible strategy-benchmark wording.
- Label starter reports as smoke artifacts.
- Ensure `toy_code_repair` is not shown as an implemented success path.
- Keep MVP strategy set consistent across README, AGENTS, design docs, and review packet.

Artifacts:

- Updated `pyproject.toml`, README, AGENTS, design docs.
- Smoke JSONL / Markdown report that can run from a fresh clone.

Exit gate:

```text
[x] No public default artifact shows repair stub success.
[x] Package metadata matches README positioning.
[x] Starter report says smoke, not final benchmark evidence.
[x] Future-agent instructions point to this execution plan.
```

### Phase 1: Benchmark Spine Contracts

Goal: make the benchmark loop real before scaling case count.

Implementation content:

- Add `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`, and extend `CaseSpec` with family and strategy-difference dimensions.
- Add `ToolSpec` with input / output schema, risk level, side effect, cost estimate, and MCP exposure metadata.
- Add `ToolExecutor` that wraps all tool calls and records latency, cost proxy inputs, context chars, and structured errors.
- Add `AgentStrategy` protocol and minimum `ReactStrategy`, `PlanExecuteStrategy`, `VerifyThenAnswerStrategy` skeletons.
- Add independent grader skeleton and remove success decisions from kernel branch logic.
- Add multi-strategy CLI support.

Artifacts:

- Unit tests for schema validation, tool manifest export, ToolExecutor traces, and independent grading.
- 8-10 seed cases across retrieval depth, verification timing, and budget pressure.
- JSONL traces where at least three strategies run on the same cases.

Exit gate:

```text
[ ] Same case runs across at least three strategies.
[ ] Tool sequences differ across strategies on at least three cases.
[ ] Grader result is stored separately from agent final answer.
[ ] Tool manifest exports schema, risk, cost, and MCP exposure fields.
```

### Phase 2: Strategy-Difference Case Suite

Goal: create case quality before increasing report sophistication.

Implementation content:

- Expand to 20 MVP core cases, then 20-30 only if strategy splits remain meaningful.
- Author every case with one or more declared dimensions: retrieval depth, verification timing, budget pressure, adversarial context, tool boundary.
- Add adversarial context negative controls and poisoned / distractor documents.
- Add verification tools such as `verify_citation` and `check_answer_support`.
- Start failure taxonomy from real failed runs.

Artifacts:

- Case catalog with dimensions and intended strategy split.
- By-family metrics and unsupported-answer metrics.
- At least one flagship case card: adversarial context where `verify_then_answer` beats `react`.

Exit gate:

```text
[ ] At least 20 cases total.
[ ] At least 20% of cases fail or exceed budget under at least one strategy.
[ ] `unsupported_answer_rate` differs between `react` and `verify_then_answer`.
[ ] Report includes by-family metrics and initial failure taxonomy.
```

### Phase 2.5: Showcase Entry Upgrade

Goal: keep public presentation aligned before the full ablation report grows.

Implementation content:

- Keep README as a short landing page, not a design memo.
- Update `reports/README.md` whenever a new report, trace, manifest, or case-card artifact is added.
- Add a first case card once a case demonstrates a real strategy split.
- Decide whether Markdown is enough or a static showcase page is needed after Phase 3.

Exit gate:

```text
[ ] README can be understood in 3 minutes.
[ ] Reports index links generated artifacts and planned final artifacts.
[ ] At least one visible artifact shows a strategy difference beyond cost-only rows.
```

### Phase 3: Cost-Aware Control Policy

Goal: turn `context_budget_agent` into the project’s algorithm-signal anchor.

Implementation content:

- Implement `ContextBudgetStrategy` with explicit `BudgetSpec` consumption.
- Use MVP VoI heuristic:

```text
chunk_value = query_relevance * source_reliability * novelty
chunk_cost = estimated_context_chars + tool_cost
selection_score = chunk_value / max(chunk_cost, 1)
```

- Track `cost_proxy`, context chars, tool calls, verification calls, and budget violations per run.
- Generate success-cost frontier and Pareto / dominated strategy analysis.
- Document cases where lower cost causes missed evidence.

Artifacts:

- `reports/agent_strategy_ablation.md`.
- `reports/context_budget_frontier.md`.
- Top 3 case cards linked from README.

Exit gate:

```text
[ ] Four MVP strategies are compared in one run.
[ ] Report shows success, tool calls, context chars, cost proxy, unsupported answer rate, and budget violation rate.
[ ] `context_budget` has lower cost on some cases and explicit failure modes.
[ ] Pareto frontier identifies dominated strategies or dominated runs.
```

### Phase 4: Public Packaging And MCP Evidence

Goal: make the finished spine easy to inspect in three minutes.

Implementation content:

- Add README claim-evidence table linking to reports, traces, and representative case cards.
- Add architecture diagram or concise module map.
- Add FastMCP adapter for 2-3 core tools only after in-process ToolSpec is stable.
- Add resume bullets that avoid enterprise security, MCP-native, or LLM-improvement overclaims.

Artifacts:

- Final README evidence table.
- Tool manifest and optional FastMCP smoke transcript.
- Stable sample command set for reviewers.

Exit gate:

```text
[ ] README claims map to concrete artifacts.
[ ] Reports link to trace files or reproducible commands.
[ ] FastMCP is either demonstrated or clearly marked planned.
[ ] Project story remains strategy benchmark first.
```

### Phase 5: Optional Expansion

Goal: add secondary environments only when they strengthen the ablation report.

Candidate content:

- `reflective_agent` retry / repair with real grader-triggered retry.
- 2-3 core tools exposed through FastMCP if not completed in Phase 4.
- Optional cheap LLM-backed planner comparison.
- Small sensitive-action balanced family.
- 3-5 bounded coding fixture cases.

Expansion gate:

```text
[ ] New feature changes at least one metric, trace, report section, or case card.
[ ] New feature does not replace the strategy benchmark spine.
[ ] New claim is added to the claim-evidence table with required artifacts.
```

## 6. First Implementation Ticket Queue

| ID | Ticket | Depends On | Output |
|---|---|---|---|
| P1-A | Add schema contracts | Phase 0.5 | `BudgetSpec`, `ExpectedOutcome`, `GraderSpec`, tests. |
| P1-B | Add ToolSpec and manifest export | Phase 0.5 | Manifest JSON with schema / risk / cost / MCP exposure. |
| P1-C | Add ToolExecutor | P1-B | Per-call trace, cost and context accounting. |
| P1-D | Add AgentStrategy protocol | P1-A, P1-C | Kernel uses strategy object instead of strategy label. |
| P1-E | Add independent grader | P1-A | `grader_result` separated from final answer. |
| P1-F | Add multi-strategy CLI | P1-D, P1-E | `--strategies react,plan_execute,verify_then_answer`. |
| P2-A | Author dimension-led seed cases | P1-A | 8-10 seed cases with intended strategy splits. |
| P2-B | Add verification tools | P1-B, P1-C | `verify_citation`, `check_answer_support`. |
| P3-A | Implement context budget policy | P1-D, P2-A | VoI selection, budget accounting, failure explanations. |
| P3-B | Generate ablation report | P1-E, P3-A | leaderboard, by-family metrics, frontier. |

## 7. Anti-Drift Rules

- Do not add a new feature unless it appears in at least one trace, metric, report, or case card.
- Do not expand case count if the current cases do not separate strategies.
- Do not call a run an ablation unless the same cases run across multiple strategies.
- Do not let the agent kernel set final success after Phase 1; success belongs to the grader.
- Do not call the project MCP-native before a real MCP adapter is implemented and demonstrated.
- Do not add UI, vector database plumbing, large guardrail libraries, A2A, or full coding-agent behavior in MVP.
- Do not use `toy_code_repair` as a public success example until it applies a patch and reruns tests.
- Do not make sensitive-action policy the main project story; it is a bounded task family.
- Do not let README become a long positioning memo; move rationale to design docs.

## 8. Reviewer-Facing Definition Of Done

For a public MVP, a reviewer should be able to do this:

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --strategies react,plan_execute,verify_then_answer,context_budget --out reports/mvp_run.jsonl
python scripts/generate_report.py --run reports/mvp_run.jsonl --out reports/agent_strategy_ablation.md
python scripts/export_tool_manifest.py --out reports/tool_manifest.json
```

Then the reviewer should see:

- the same cases under four strategies.
- structured tool calls with cost and context accounting.
- a tool manifest with schema, risk, side-effect, cost, and MCP exposure metadata.
- independent grader results.
- by-strategy and by-family metrics.
- unsupported-answer and budget-violation rates.
- a success-cost frontier.
- at least three case cards explaining real failures or tradeoffs.

Until this is true, the repository remains a starter skeleton plus design plan, not a completed benchmark.
