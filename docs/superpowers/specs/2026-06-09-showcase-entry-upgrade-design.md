# Showcase Entry Upgrade Design

> Date: 2026-06-09
> Status: proposed spec for user review
> Scope: Phase 2.5 showcase entry upgrade for ContextGuard Agent Lab

## 1. Objective

Upgrade the current seed benchmark artifacts into a reviewer-friendly showcase package. The package should let a portfolio reviewer understand the project in about three minutes and then inspect deeper evidence through generated reports, JSONL traces, and the tool manifest.

The implementation should keep the project artifact-driven. Markdown reports, JSONL run records, tool manifest JSON, and README links remain the primary display layer.

## 2. Current Baseline

The repository already has these working artifacts:

- `reports/agent_strategy_ablation.jsonl` with 36 run records across 9 cases and 4 MVP strategies.
- `reports/agent_strategy_ablation.md` with by-strategy, by-family, success-cost, split, detail, and failure sections.
- `reports/tool_manifest.json` with MCP-compatible in-process tool contracts.
- `reports/sample_report.md` and `reports/sample_run.jsonl` for smoke validation.
- `reports/README.md` as the current artifact index.

The current gap is presentation depth. The ablation report shows raw differences, while reviewers still need a concise explanation of representative case splits and budget tradeoffs.

## 3. Chosen Approach

Use lightweight generators plus Markdown artifacts:

1. Add `scripts/generate_case_cards.py`.
2. Add `scripts/generate_frontier_report.py`.
3. Generate `reports/case_cards.md`.
4. Generate `reports/context_budget_frontier.md`.
5. Update `reports/README.md` with the new artifacts and regeneration commands.
6. Update `README.md` with a short claim-evidence table that links public claims to concrete artifacts.

This approach keeps showcase quality tied to reproducible benchmark outputs and avoids adding heavy UI before the report data matures.

## 4. Artifact Design

### 4.1 `reports/case_cards.md`

Purpose: explain representative strategy differences in a compact, reviewer-readable format.

Input:

- `reports/agent_strategy_ablation.jsonl`
- `data/benchmark/cases.sample.jsonl`

Selection policy:

- Prefer cases where strategies have different success outcomes.
- Prefer one case from each high-value dimension when available:
  - `retrieval_depth`
  - `verification_timing`
  - `budget_pressure`
  - `adversarial_context`
- Keep the initial output to 3-5 cards so it remains quick to scan.

Each card should include:

- Case id, family, dimensions, and intended split.
- User query, with safe public toy content only.
- Winners and losers by strategy.
- Tool sequence per strategy.
- Cost, context, unsupported flag, budget violation flag, and grader reason.
- A short interpretation explaining what the case demonstrates.

### 4.2 `reports/context_budget_frontier.md`

Purpose: make the success-cost tradeoff visible and give `context_budget` a clear current status before the later VoI policy upgrade.

Input:

- `reports/agent_strategy_ablation.jsonl`

Sections:

1. Overview with source trace, run count, strategy count, and case count.
2. Success-cost table by strategy.
3. Pareto / dominated analysis using success rate and mean cost.
4. Context budget focus with current wins, losses, and observed limitations.
5. Next policy upgrade notes for explicit Value-of-Information scoring.

Dominance rule:

A strategy is dominated when another strategy has equal or higher success rate and equal or lower mean cost, with at least one strict improvement.

### 4.3 README claim-evidence table

Purpose: connect top-level project claims to inspection artifacts.

Example claims:

- Same cases compare multiple agent strategies.
- Tool use is exposed through an MCP-compatible boundary.
- Independent grading is stored separately from the agent answer.
- Context and budget tradeoffs are measurable.
- Representative strategy splits are inspectable through case cards.

Each row should link to a concrete artifact path.

### 4.4 `reports/README.md`

Purpose: stay the durable artifact index.

Updates:

- Add generated `case_cards.md` and `context_budget_frontier.md` entries.
- Add commands to regenerate the ablation, case cards, frontier report, and manifest.
- Keep planned static page clearly marked as optional future work.

## 5. Script Design

### 5.1 `scripts/generate_case_cards.py`

CLI shape:

```powershell
python scripts/generate_case_cards.py --run reports/agent_strategy_ablation.jsonl --cases data/benchmark/cases.sample.jsonl --out reports/case_cards.md
```

Implementation notes:

- Reuse existing JSONL reading helpers where practical.
- Load `CaseSpec` rows through the benchmark loader.
- Group run records by `case_id`.
- Select cases with mixed success outcomes first.
- Render deterministic Markdown ordering.
- Keep comments in English to match the codebase style.

### 5.2 `scripts/generate_frontier_report.py`

CLI shape:

```powershell
python scripts/generate_frontier_report.py --run reports/agent_strategy_ablation.jsonl --out reports/context_budget_frontier.md
```

Implementation notes:

- Reuse `contextguard_agent_lab.eval.metrics.summarize`.
- Group records by strategy.
- Compute dominated strategies with the same rule as the existing report, or factor a helper only if duplication becomes risky.
- Render deterministic Markdown ordering.
- Highlight `context_budget` from actual run data.

## 6. Testing And Verification

Add focused tests where they increase confidence without making the project heavy:

- Test case-card selection prefers split cases and stable ordering.
- Test frontier dominance classification.
- Test generated Markdown contains expected section headers and key strategy names.

Default verification commands:

```powershell
python -m compileall -q src scripts tests
python -m unittest discover -s tests
python scripts/run_eval.py --case-limit 3 --strategies react,plan_execute,verify_then_answer,context_budget --out reports/sample_run.jsonl
python scripts/generate_report.py --run reports/sample_run.jsonl --out reports/sample_report.md
python scripts/export_tool_manifest.py --out reports/tool_manifest.json
python scripts/run_eval.py --strategies react,plan_execute,verify_then_answer,context_budget --out reports/agent_strategy_ablation.jsonl
python scripts/generate_report.py --run reports/agent_strategy_ablation.jsonl --out reports/agent_strategy_ablation.md
python scripts/generate_case_cards.py --run reports/agent_strategy_ablation.jsonl --cases data/benchmark/cases.sample.jsonl --out reports/case_cards.md
python scripts/generate_frontier_report.py --run reports/agent_strategy_ablation.jsonl --out reports/context_budget_frontier.md
```

## 7. Scope Boundaries

In scope:

- Generated Markdown showcase artifacts.
- README and reports index updates.
- Small tests for deterministic report generation.

Out of scope for this spec:

- Static HTML showcase page.
- FastMCP adapter work.
- LLM-backed planner.
- Reflective repair.
- Expanding the case suite beyond what is needed to render current representative cards.
- Changing core strategy behavior.

## 8. Risks And Mitigations

| Risk | Mitigation |
|---|---|
| Reports overclaim seed-suite evidence | Keep wording as seed / MVP-oriented evidence and avoid final-benchmark language. |
| Case cards become too verbose | Limit to 3-5 representative cards and use compact tables. |
| Script logic duplicates existing report code | Reuse existing helpers where simple; duplicate small pure formatting logic only when it keeps scripts readable. |
| `context_budget` currently has shallow policy logic | Present it as current observed behavior and reserve explicit VoI policy for the next milestone. |

## 9. Acceptance Criteria

- `reports/case_cards.md` exists and includes at least three representative split cards.
- `reports/context_budget_frontier.md` exists and summarizes success-cost / Pareto observations.
- `README.md` includes a concise claim-evidence table.
- `reports/README.md` indexes both new artifacts and gives regeneration commands.
- Default validation and new report-generation commands pass.
- Public wording stays bounded to seed-suite / MVP-oriented evidence.
