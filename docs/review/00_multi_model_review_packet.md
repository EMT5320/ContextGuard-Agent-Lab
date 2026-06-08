# Multi-model Review Packet

> 使用方式：把本文发给其他模型，让它们从项目规划、岗位价值、技术可行性、评测有效性和风险收敛角度审稿。

## 1. Project summary

ContextGuard Agent Lab is an MCP-native, evidence-governed agent evaluation workbench. It aims to demonstrate a minimal auditable Agent kernel, strategy ablation, context/tool governance, sensitive-action evidence gates, and a bounded workspace repair loop.

## 2. Candidate target roles

Current target ladder:

- Stable: Agent engineer / LLM application engineer / RAG-context engineering engineer。
- Upward: Agent algorithm / application strategy algorithm engineer / Agent evaluation engineer。
- Stretch: post-training or evaluation-heavy algorithm roles where AlgoCoach provides the main evidence。
- Low priority: foundation-model pretraining or core model-training roles。

## 3. Existing portfolio context

See `docs/design/08_background_snapshot.md` for the stable sanitized snapshot.

- Company work already covers multi-agent security analysis, LLM guardrails, RAG knowledge base, file-level analysis, security microservices, and production services, but cannot be fully public.
- AlgoCoach-Flywheel covers post-training, verifier, simulator, data flywheel, evaluation infrastructure, and inference companion work.
- Loomstead covers agent runtime observability, trace, counterfactual replay, audit case cards, and high-risk tool blocking.
- ContextGuard should focus on the public gap: protocol-native agent kernel, strategy ablation, evidence-gated execution, and bounded workspace repair.

## 4. Proposed differentiator

This project should avoid becoming a generic RAG demo. The intended differentiator is:

```text
Agent kernel + MCP tool boundary + evidence-gated execution + strategy evaluation + case cards
```

## 5. Planned modules

- Benchmark: CaseSpec, corpus, workspace fixtures, policy fixtures。
- Agent strategies: react, plan-execute, reflective, guarded, context-budget。
- Tools: retrieval, workspace, sensitive action, MCP adapters。
- Governance: evidence policy, injection checks, permission profiles。
- Trace/eval: ToolCallTrace, PolicyDecision, RunRecord, metrics, reports。

## 6. Main questions for reviewers

1. Is this positioning strong enough for Agent algorithm / strategy roles?
2. Which part is over-scoped for a one-month portfolio sprint?
3. Which part is under-specified and likely to fail during implementation?
4. Does the eval contract support the claims?
5. Should toy code repair be included, or should the project stay focused on context/tool governance?
6. Is MCP a meaningful protocol boundary here, or just a label?
7. What should be cut first if time is limited?
8. What would make this repo impressive within 3 minutes of README reading?

## 7. Expected reviewer output format

```markdown
# Review: ContextGuard Agent Lab

## Verdict
- Go / revise / pivot:
- Confidence:

## Strongest parts
- ...

## Biggest risks
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

