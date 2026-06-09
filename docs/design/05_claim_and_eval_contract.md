# Claim and Eval Contract

## 1. Allowed Claims

| Claim | Required Evidence |
|---|---|
| The project implements a minimal agent strategy benchmark. | `AgentStrategy` interface, same `CaseSpec` across strategies, unit tests, sample run。 |
| Agent strategies can be compared under unified tasks. | Strategy leaderboard, per-family metrics, non-trivial success / cost differences。 |
| Tool use is exposed through an MCP-compatible boundary. | `ToolSpec`, `ToolRegistry`, `ToolExecutor`, structured tool traces; FastMCP adapter only if implemented。 |
| Context budget tradeoffs are measurable. | `context_chars_used`, `cost_proxy`, budget pressure cases, budget frontier report。 |
| Verification can reduce unsupported answers in bounded cases. | Verification-needed cases, `unsupported_answer_rate`, citation coverage, before/after strategy comparison。 |
| Reflection can recover some failures in bounded cases. | Reflective strategy retry trace, recovery cases, `reflection_recovery_rate`。 |
| Sensitive-action handling is demonstrated only as a small bounded task family. | PolicyDecision trace, allow/block/review cases, unsafe allow / false block metrics。 |

## 2. Disallowed Claims

- Production-grade enterprise security。
- Full coding agent replacement。
- General RAG framework superiority。
- Human productivity improvement without real study evidence。
- Loomstead-style observability platform replacement。
- MCP-native runtime before an actual MCP adapter is implemented and demonstrated。

## 3. Minimum Metric Contract

| Metric | Definition |
|---|---|
| `task_success_rate` | Cases with expected outcome achieved by independent grader。 |
| `mean_tool_calls` | Average tool calls per case。 |
| `cost_proxy` | Weighted tool calls + context chars + verification calls。 |
| `context_chars_used` | Approximate context characters consumed by retrieved / read content。 |
| `budget_violation_rate` | Cases where strategy exceeds declared budget。 |
| `citation_coverage` | Required citation evidence found / required evidence total。 |
| `unsupported_answer_rate` | Final answers not supported by retrieved evidence。 |
| `verification_call_rate` | Fraction of cases where verification tools are invoked。 |
| `reflection_recovery_rate` | Failed first attempts recovered by reflection。 |
| `unsafe_allow_rate` | Sensitive action allowed while required evidence is missing。 |
| `false_block_rate` | Benign or fully evidenced sensitive action blocked。 |

## 4. Case Card Contract

Each public case card must include:

- task and case family。
- strategy and budget。
- important tool calls。
- grader / verification result。
- success / failure。
- what the strategy comparison proves。
- honest limitation。

## 5. Review Gate

Before implementation sprint, at least one external/model review should challenge:

1. Whether the pivot away from Loomstead overlap is sufficient。
2. Whether the strategy set creates real ablation rather than labels。
3. Whether eval validity supports the claims。
4. Whether MCP-compatible is meaningful before FastMCP。
5. Whether the MVP fits one month without starving AlgoCoach。
