# Claim and Eval Contract

## 1. Allowed claims

| Claim | Required evidence |
|---|---|
| The project implements a minimal auditable Agent kernel. | AgentState, ToolCallTrace, RunRecord, unit tests, sample run. |
| Agent strategies can be compared under unified tasks. | Same CaseSpec across multiple strategies, strategy leaderboard. |
| Evidence-gated sensitive tool execution is implemented. | PolicyDecision trace, missing evidence cases, unsafe allow metric. |
| Workspace repair loop is demonstrated on bounded fixtures. | fixture repo, failing test, patch trace, rerun result. |
| Context governance tradeoffs are measurable. | context budget metric, retrieval/citation metric, cost proxy. |

## 2. Disallowed claims

- Production-grade enterprise security.
- Full coding agent replacement.
- General RAG framework superiority.
- Real-world vulnerability or SOC automation quality.
- Human productivity improvement without real study evidence.

## 3. Minimum metric contract

| Metric | Definition |
|---|---|
| `task_success_rate` | Cases with expected outcome achieved. |
| `mean_tool_calls` | Average tool calls per case. |
| `repair_success_rate` | Code repair cases fixed after one or more attempts. |
| `unsafe_allow_rate` | Sensitive action allowed while required evidence is missing. |
| `false_block_rate` | Benign or fully evidenced action blocked. |
| `evidence_coverage` | Observed required evidence / total required evidence. |
| `cost_proxy` | Approximate context tokens + tool calls. |

## 4. Case card contract

Each public case card must include:

- task and case type。
- strategy。
- important tool calls。
- policy decision when applicable。
- success / failure。
- what the case proves。
- honest limitation。

## 5. Review gate

Before implementation sprint, at least one external/model review should challenge:

1. Positioning clarity。
2. Differentiation from existing RAG/guardrail frameworks。
3. Eval validity。
4. Feasibility within one month。
5. Interview value for Agent algorithm roles。
