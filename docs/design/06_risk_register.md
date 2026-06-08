# Risk Register

## 1. Top risks

| ID | Risk | Symptom | Mitigation | Kill / pivot criterion |
|---|---|---|---|---|
| R1 | Scope drifts into another RAG platform | UI, vector DB plumbing, product features dominate | Keep CLI + reports; only keep RAG pieces needed for Agent eval | More than one week spent on non-eval RAG plumbing |
| R2 | Agent kernel too shallow for algorithm roles | Only tool calling demo, no strategy comparison | Require at least 4 strategies and ablation report | No strategy leaderboard by W2 end |
| R3 | Guardrail repeats company experience without public novelty | Many policy examples, little trace/eval | Focus on evidence contract + unsafe allow / false block | No PolicyDecision trace in report |
| R4 | Coding-agent slice becomes too large | Trying to clone Codex/Claude Code | Keep bounded toy fixtures first | Real repo tasks block fixture milestones |
| R5 | Eval lacks validity | Metrics easy to game, cases too toy | Add bad-case taxonomy and reviewer questions | Case cards fail to convince reviewers |
| R6 | Public claim overreaches | README sounds production-grade | Maintain claim contract and honest boundaries | Claims cannot map to artifacts |
| R7 | Time competes with AlgoCoach | Too much implementation before review | Freeze design first, implement gates later | AlgoCoach P0 evidence work starves |

## 2. Lessons imported from prior project work

- Use case-card-first presentation for public readers.
- Keep evidence snippets and trace artifacts close to claims.
- Avoid research claims without strong evaluation evidence.
- Preserve a narrow final story early, then expand only after validation.

## 3. Review prompts for risk discovery

- Which module should be cut first if time halves?
- Which claim is easiest for a reviewer to attack?
- Which metric is most likely to be misleading?
- Which part overlaps too much with existing projects?
- Which part best signals Agent algorithm ability?
