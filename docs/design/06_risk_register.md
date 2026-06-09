# Risk Register

## 1. Top Risks

| ID | Risk | Symptom | Mitigation | Kill / Pivot Criterion |
|---|---|---|---|---|
| R1 | Drifts into Loomstead overlap | Trace / audit / case-card story becomes the main pitch | Keep observability as support only; main report is strategy ablation | README sounds like Agent Behavior Observatory |
| R2 | Agent strategies are labels only | Same tool calls and same success across all strategies | Require real `AgentStrategy` interface and non-trivial behavior deltas | No strategy leaderboard with differences by P2 end |
| R3 | MCP becomes a label | Tool registry exists but no schema / adapter / metadata | Implement `ToolSpec` first; call it MCP-compatible, not MCP-native | Cannot show tool schema or adapter plan |
| R4 | Eval lacks validity | Cases are too easy; all strategies get 100% | Add failure cases, negative controls, independent grader | No bad-case taxonomy after MVP cases |
| R5 | Scope drifts into RAG platform | Vector DB / embeddings / UI dominate | Keep RAG as task environment | More than one week spent on non-eval RAG plumbing |
| R6 | Coding-agent slice becomes too large | Trying to clone Codex / Claude Code | Keep coding fixture optional and bounded | Coding work blocks strategy benchmark milestones |
| R7 | Public claim overreaches | README promises enterprise security or full MCP-native runtime | Maintain claim contract and honest boundaries | Claims cannot map to artifacts |
| R8 | Time competes with AlgoCoach | Too much implementation before review | Freeze design first, implement gates later | AlgoCoach P0 evidence work starves |
| R9 | Algorithm signal stays too weak | Strategies look like if-else engineering rather than control policies | Upgrade context budget to VoI policy and report Pareto frontier | No success-cost frontier or policy explanation by Phase 3 |
| R10 | LLM-backed strategy enters too early | Non-determinism obscures benchmark validity | Keep deterministic MVP; add LLM planner only after grader/report are stable | LLM integration blocks P1/P2 gates |

## 2. Lessons Imported From Prior Project Work

- Use case-card-first presentation only after a strong report exists。
- Keep evidence snippets and trace artifacts close to claims。
- Avoid research claims without strong evaluation evidence。
- Preserve a narrow final story early, then expand only after validation。
- Do not make depth the only goal; design for 3-minute reviewer comprehension from day one。

## 3. Current Cut Line

Must-have:

- Strategy interface。
- ToolSpec / ToolExecutor。
- Independent grader。
- 4 strategies with real behavior differences。
- 20-30 high-quality cases。
- Strategy ablation report。
- VoI-based context budget policy。

Should-have:

- Context budget frontier。
- Adversarial context family。
- Verify-then-answer comparison。
- Tool manifest export with MCP-compatible schema metadata。

Stretch:

- Minimal FastMCP adapter。
- Reflective repair beyond retry。
- Small coding fixture family。
- Hosted LLM planner。

Cut:

- A2A。
- Heavy UI。
- Full coding agent。
- Generic RAG platform。
- Large guardrail library。

## 4. Review Prompts For Risk Discovery

- Which module overlaps most with Loomstead in actual public presentation?
- Which strategy could be removed without weakening the ablation story?
- Which metric is easiest to game?
- Which case family gives the strongest Agent algorithm signal?
- What would make this repo impressive within 3 minutes?
