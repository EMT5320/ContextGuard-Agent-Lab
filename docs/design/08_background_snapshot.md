# Background Snapshot

> Updated: 2026-06-08
> Purpose: provide a stable, sanitized context snapshot for multi-model design review. This file avoids company-private data and only keeps portfolio-level positioning.

## 1. Current market positioning

Primary positioning:

```text
LLM application / Agent engineering candidate with agent evaluation, post-training evaluation, security-domain production experience, and inference-service engineering background.
```

Current target ladder:

| Tier | Target roles | Notes |
|---|---|---|
| Stable | LLM application engineer, Agent engineer, RAG / context engineering engineer | Existing company and portfolio evidence already supports this tier. |
| Upward | Agent algorithm engineer, application strategy algorithm engineer, Agent evaluation engineer | This project should strengthen strategy ablation, eval validity, and agent-kernel design signals. |
| Stretch | Post-training / evaluation-heavy algorithm roles | AlgoCoach carries most evidence; ContextGuard should provide complementary agent-eval artifacts. |
| Low priority | Foundation model pretraining / core model training roles | Current public portfolio does not target this as the main path. |

## 2. Existing evidence portfolio

| Asset | Current evidence | Public-showcase constraint |
|---|---|---|
| Company work | Multi-agent security analysis, LLM guardrails, RAG knowledge base, file-level analysis, security microservices, production delivery | Strong real-world evidence, but most details cannot be public. |
| AlgoCoach-Flywheel | Post-training workflow, verifier, simulator, data flywheel, evaluation infrastructure, inference companion | Strong research/eval signal; claims must remain evidence-bounded. |
| Loomstead | Agent runtime observability, trace, counterfactual replay, audit case cards, high-risk tool blocking | Frozen as a bounded Agent Behavior Observatory portfolio artifact. |
| ContextGuard Agent Lab | Planned public artifact for MCP-style tool boundary, agent kernel, evidence-gated execution, strategy evaluation, workspace repair loop | Should stay small, auditable, and report-driven. |

## 3. Updated gap analysis

Already covered well:

- Real production RAG and guardrail experience from company work.
- Agent runtime and trace observability from Loomstead.
- Post-training / simulator / verifier / data governance from AlgoCoach.
- Inference and evaluation infrastructure from AlgoCoach and company work.

Still under-covered in public artifacts:

- Protocol-native tool boundary: MCP-style retrieval / workspace / sensitive tools.
- Minimal but complete Agent kernel: plan / act / observe / reflect / repair.
- Agent strategy comparison: ReAct, plan-execute, reflective, guarded, context-budget.
- Unified benchmark and trace artifacts for Agent behavior.
- Workspace repair loop as a bounded coding-agent-like demonstration.
- Evidence-gated sensitive tool execution with measurable unsafe allow / false block rates.

Lower-ROI areas for this project:

- Generic RAG product platform.
- Generic vector database plumbing.
- Large guardrail rule library.
- Full Security Copilot clone.
- Full Codex / Claude Code replacement.
- A2A platform implementation.
- Heavy UI work.

## 4. Implications for project design

The project should keep Agent kernel and Agent evaluation as the main spine:

```text
Agent kernel + MCP-style tools + evidence policy + strategy ablation + trace/report/case cards
```

RAG and guardrails should serve as task environments and evaluation dimensions. They should not dominate the repo as separate product surfaces.

## 5. Review focus

When reviewers evaluate this project, they should specifically challenge:

1. Whether the project is strong enough for Agent algorithm / application strategy roles.
2. Whether strategy ablation is more valuable than additional RAG pipelines.
3. Whether toy code repair is enough to signal coding-agent-like ability.
4. Whether evidence-gated execution is meaningfully integrated into the agent loop.
5. Whether claims can be fully mapped to metrics, traces, reports, and case cards.
