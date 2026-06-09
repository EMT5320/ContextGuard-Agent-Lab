# Multi-model Review Packet

> 使用方式：把本文发给其他模型，让它们从项目规划、岗位价值、技术可行性、评测有效性和风险收敛角度审稿。本文对应 2026-06-09 后的新版 pivot 方案。

## 1. Project Summary

ContextGuard Agent Lab is now framed as an MCP-compatible Agent Strategy Benchmark. It aims to compare agent control policies under unified tasks, structured tool contracts, verification requirements, and context / tool budget constraints.

The previous `evidence-governed workbench` framing was revised because Loomstead already covers Agent Behavior Observatory, trace provenance, counterfactual replay, and audit failure-analysis.

## 2. Candidate Target Roles

Current target ladder:

- Stable: Agent engineer / LLM application engineer / RAG-context engineering engineer。
- Upward: Agent algorithm / application strategy algorithm engineer / Agent evaluation engineer。
- Stretch: post-training or evaluation-heavy algorithm roles where AlgoCoach provides the main evidence。
- Low priority: foundation-model pretraining or core model-training roles。

## 3. Existing Portfolio Context

See `docs/design/08_background_snapshot.md` for the stable sanitized snapshot.

- Company work already covers multi-agent security analysis, LLM guardrails, RAG knowledge base, file-level analysis, security microservices, and production services, but cannot be fully public。
- AlgoCoach-Flywheel covers post-training, verifier, simulator, data flywheel, evaluation infrastructure, and inference companion work。
- Loomstead covers agent runtime observability, structured trace, counterfactual replay, audit failure-analysis, and portfolio case-card packaging。
- ContextGuard should focus on the remaining public gap: MCP-compatible tool boundary, strategy ablation, context budget, verification tradeoffs, and success-cost reporting。

## 4. Proposed Differentiator

This project should avoid becoming a generic RAG demo, guardrail demo, or Loomstead duplicate. The intended differentiator is:

```text
AgentStrategy + MCP-compatible tools + verification + context budget + strategy ablation report
```

## 5. Planned Modules

- Benchmark: CaseSpec, BudgetSpec, ExpectedOutcome, GraderSpec。
- Agent strategies: react, plan-execute, verify-then-answer, reflective, context-budget。
- Tools: retrieval, verification, budget metadata, small sensitive-action set, optional MCP adapters。
- Eval: independent grader, strategy leaderboard, success-cost frontier, failure taxonomy。
- Reports: ablation report, context budget frontier, adversarial context eval, case cards。

## 6. Main Questions For Reviewers

1. Is this revised positioning strong enough for Agent algorithm / strategy roles?
2. Does it avoid real overlap with Loomstead, or does it still sound like observability / audit?
3. Which strategy set gives the strongest ablation signal for a one-month sprint?
4. Is MCP-compatible tool boundary meaningful before a FastMCP adapter is implemented?
5. Which case families should be must-have versus stretch?
6. What eval metric is easiest to game?
7. What should be cut first if time is limited?
8. What would make this repo impressive within 3 minutes of README reading?

## 7. Expected Reviewer Output Format

```markdown
# Review: ContextGuard Agent Lab Revised Scope

## Verdict
- Go / revise / pivot:
- Confidence:

## Strongest parts
- ...

## Biggest risks
- ...

## Loomstead overlap risk
- ...

## Missing higher-level role signals
- ...

## Over-scoped parts to cut
- ...

## Recommended final scope
- Must-have:
- Should-have:
- Stretch:
- Cut:

## Concrete changes to docs / architecture / eval
- ...
```
