# Showcase Entry Design

> Status: active design constraint.
> Purpose: make ContextGuard understandable within 3 minutes without building a heavy UI.

## 1. Problem

ContextGuard can easily become deep but hard to show. A portfolio reviewer should not need to read review history, project-positioning debates, or long negative-scope explanations before seeing what the project does.

The showcase layer must answer these questions first:

1. What does the project run?
2. What artifact proves it ran?
3. What strategy difference is visible?
4. What can I inspect next?

## 2. Display Strategy

The display layer has three tiers:

| Tier | Entry | Role |
|---|---|---|
| Landing | `README.md` | 3-minute explanation and runnable commands. |
| Artifact index | `reports/README.md` | Links generated reports, traces, manifests, and future case cards. |
| Optional static page | `docs/showcase/` or `site/` | Later single-page visual summary if Markdown is not enough. |

Heavy interactive UI remains out of scope. A lightweight static page is allowed if it directly renders existing reports / JSONL / manifest artifacts.

## 3. README Contract

README should stay short and concrete:

| Section | Purpose |
|---|---|
| One-line summary | Say what runs and what is compared. |
| What It Shows | Map capabilities to artifacts. |
| 3-Minute Run | Provide commands that generate visible outputs. |
| Inspect The Results | Point to report, JSONL trace, manifest, and cases. |
| How It Works | Show the pipeline in one diagram. |
| Current Status | Say what is implemented and what remains starter-only. |
| Next Milestones | Tell future agents and reviewers what comes next. |

README should not carry long portfolio-gap analysis, review synthesis, or repeated disallowed claims. Those belong in `docs/design/` and `docs/review/`.

## 4. Artifact Contract

Every major feature should produce at least one reviewer-visible artifact:

| Feature | Required Display Artifact |
|---|---|
| Strategy execution | JSONL run records and Markdown row in a report. |
| Tool boundary | Tool manifest JSON. |
| Independent grading | `grader_result` fields and report reason column. |
| Case design | Case catalog or case cards with dimensions. |
| Budget policy | Success-cost table and frontier report. |
| Failure analysis | Failure taxonomy and representative case cards. |

If a feature cannot be shown through these artifacts, it should not be treated as a public milestone.

## 5. Optional Static Showcase

A future static showcase can be useful after Phase 2 or Phase 3. It should be a generated or static artifact, not a product UI.

Minimum page shape:

```text
Hero: same cases, different agent strategies
  -> Strategy leaderboard
  -> Success-cost scatter or table
  -> Tool manifest summary
  -> 3 representative case cards
  -> Links to JSONL traces and reports
```

Implementation guardrails:

- Use existing JSONL / Markdown / manifest outputs as data sources.
- Avoid adding backend services.
- Avoid spending time on visual polish before the report has meaningful strategy separation.
- Do not let UI replace the CLI and report workflow.

## 6. Phase Gates

| Phase | Showcase Requirement |
|---|---|
| Phase 1 | README and report index show starter contracts, manifest, smoke run, and current limitations. |
| Phase 2 | Report shows by-family metrics and at least one case card. |
| Phase 3 | README links ablation report, context-budget frontier, and top case cards. |
| Phase 4 | Optional static page or final public package can be added if it reuses existing artifacts. |

## 7. Anti-Drift Rules

- Keep README as a landing page, not a design memo.
- Move portfolio positioning, overlap analysis, and review debates into docs.
- Every generated report should have a short index entry in `reports/README.md`.
- Do not introduce frontend work that lacks trace / metric / report data to display.
- Treat showcase quality as part of each phase gate, not as last-week polish.
