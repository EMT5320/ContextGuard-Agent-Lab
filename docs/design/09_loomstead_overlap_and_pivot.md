# Loomstead Overlap and Pivot Decision

## 1. Why This Document Exists

The first ContextGuard concept was framed as an `MCP-native, evidence-governed agent evaluation workbench`. After comparing it with Loomstead, that framing created real portfolio overlap risk.

This document records the revised decision: ContextGuard should not compete with Loomstead on observability, trace, or audit storytelling. It should become an MCP-compatible Agent Strategy Benchmark.

## 2. Loomstead Evidence Actually Verified

The overlap audit should distinguish completed public evidence from historical plans.

Checked commands and artifacts:

```powershell
npm.cmd run portfolio:check
npm.cmd run eval:audit
npm.cmd run eval:domain
```

Confirmed Loomstead strengths:

- Portfolio entry and case-card path are present and verified。
- Agent Behavior Observatory is the frozen public story。
- Runtime path `MotivationEngine -> ToolExecutor -> ResultObserver` is implemented。
- `phase2.trace.v1`, `sourceEventIds`, `traceRefs`, candidate scores, and observer surfaces support behavior provenance。
- Audit suite covers 5 high-risk scenarios x 5 baselines and has reviewer packets。
- Real LLM audit smoke covers 5 scenarios x 2 evidence conditions, 10/10 passed。
- Domain suite includes 8 coding dry-run scenarios, but these are secondary validation rather than the main public story。

## 3. Confirmed Overlap

ContextGuard should avoid making these its main story:

| Area | Loomstead Status | ContextGuard Decision |
|---|---|---|
| Agent behavior observability | Strong public story | Do not duplicate。 |
| Trace provenance | Implemented and showcased | Use traces only as report support。 |
| Counterfactual evidence removal | Implemented and documented | Do not make evidence removal the core novelty。 |
| High-risk tool audit | Strong failure-analysis case | Keep sensitive action as small case family only。 |
| Case-card-first packaging | Loomstead already uses it | Use case cards after ablation report, not as main identity。 |

## 4. Partial Overlap

| Area | Loomstead Reality | ContextGuard Opportunity |
|---|---|---|
| Coding fixtures | 8 dry-run domain scenarios exist, but not a full coding-agent showcase | Only add bounded coding cases if they strengthen strategy ablation。 |
| Budget traces | Loomstead records decision budget traces | ContextGuard can study budget as a control policy across strategies。 |
| Eval pipeline | Loomstead has eval/export artifacts | ContextGuard should produce strategy leaderboard and success-cost frontier。 |

## 5. Non-overlap and New Spine

ContextGuard should own these gaps:

- MCP-compatible `ToolSpec` / `ToolExecutor` as reusable protocol boundary。
- Standard `AgentStrategy` abstraction and multi-strategy CLI。
- Strategy ablation under identical cases。
- Verification-before-answer versus direct answer tradeoff。
- Context budget and tool budget frontier。
- Adversarial context cases for context engineering。

Revised spine:

```text
AgentStrategy + ToolSpec/ToolExecutor + MCP-compatible boundary + verification + context budget + ablation report
```

## 6. Decision

ContextGuard is not cut. It is pivoted.

Accepted:

- Keep current repository and deterministic starter skeleton。
- Rewrite public positioning to `MCP-compatible Agent Strategy Benchmark`。
- Prioritize strategy implementation, independent grading, and ablation report。
- Keep sensitive action as a small environment, not a main claim。

Rejected:

- Building another observability-first agent runtime。
- Making audit / evidence gate the core differentiator。
- Starting with workspace repair or full coding-agent ambitions。
- Claiming MCP-native before adapter evidence exists。

## 7. Review Checklist

Future reviewers should challenge:

- Does the README still sound like Loomstead?
- Are strategy differences visible in tool calls and metrics?
- Does `context_budget_agent` produce a meaningful frontier rather than just fewer calls?
- Is MCP-compatible backed by concrete schema and adapter plan?
- Are case families chosen for strategy signal rather than trend stuffing?
