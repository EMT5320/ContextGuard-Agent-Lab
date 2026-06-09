# Background Snapshot

> Updated: 2026-06-09
> Purpose: provide a stable, sanitized context snapshot for multi-model design review. This file avoids company-private data and only keeps portfolio-level positioning.

## 1. Current Market Positioning

Primary positioning:

```text
LLM application / Agent engineering candidate with agent evaluation, post-training evaluation, security-domain production experience, and inference-service engineering background.
```

Current target ladder:

| Tier | Target Roles | Notes |
|---|---|---|
| Stable | LLM application engineer, Agent engineer, RAG / context engineering engineer | Existing company and portfolio evidence already supports this tier. |
| Upward | Agent algorithm engineer, application strategy algorithm engineer, Agent evaluation engineer | ContextGuard should strengthen strategy ablation, context budget, MCP-compatible tool boundary, and eval validity. |
| Stretch | Post-training / evaluation-heavy algorithm roles | AlgoCoach carries most evidence; ContextGuard provides complementary agent-control artifacts. |
| Low priority | Foundation model pretraining / core model training roles | Current public portfolio does not target this as the main path. |

## 2. Existing Evidence Portfolio

| Asset | Current Evidence | Public-showcase Constraint |
|---|---|---|
| Company work | Multi-agent security analysis, LLM guardrails, RAG knowledge base, file-level analysis, security microservices, production delivery | Strong real-world evidence, but most details cannot be public. |
| AlgoCoach-Flywheel | Post-training workflow, verifier, simulator, data flywheel, evaluation infrastructure, inference companion | Strong research/eval signal; claims must remain evidence-bounded. |
| Loomstead | Agent runtime, structured trace, counterfactual replay, audit failure-analysis, portfolio case cards; coding dry-run exists as secondary validation | Frozen as Agent Behavior Observatory; should not be duplicated by ContextGuard. |
| ContextGuard Agent Lab | Planned public artifact for MCP-compatible tool boundary, strategy ablation, context budget, verification tradeoffs, success-cost reporting | Should stay small, benchmark-driven, and report-first. |

## 3. Updated Gap Analysis

Already covered well:

- Real production RAG and guardrail experience from company work。
- Agent runtime and behavior observability from Loomstead。
- Trace / audit / failure-analysis packaging from Loomstead。
- Post-training / simulator / verifier / data governance from AlgoCoach。
- Inference and evaluation infrastructure from AlgoCoach and company work。

Still under-covered in public artifacts:

- MCP-compatible tool boundary shown as reusable tool contracts。
- Standardized AgentStrategy comparison under the same cases。
- Context budget / cost-aware agent control policies。
- Verification-before-answer tradeoffs in RAG / adversarial context tasks。
- Reported success-cost frontier and failure taxonomy for agent strategies。

Lower-ROI areas for this project:

- Generic RAG product platform。
- Generic vector database plumbing。
- Large guardrail rule library。
- Full Security Copilot clone。
- Full Codex / Claude Code replacement。
- Loomstead-style observability / audit case-card pipeline。
- A2A platform implementation。
- Heavy UI work。

## 4. Implications For Project Design

The project should keep Agent strategy evaluation as the main spine:

```text
AgentStrategy + MCP-compatible tools + verification + context budget + strategy ablation report
```

RAG, adversarial context, sensitive actions, and coding fixtures should serve as task environments. They should not dominate the repo as separate product surfaces.

## 5. Review Focus

When reviewers evaluate this project, they should specifically challenge:

1. Whether the project is strong enough for Agent algorithm / application strategy roles。
2. Whether the revised scope avoids real overlap with Loomstead。
3. Whether strategy ablation is more valuable than additional RAG pipeline work。
4. Whether MCP-compatible tool boundary is concrete enough before FastMCP。
5. Whether claims can be fully mapped to metrics, reports, traces, and case cards。
