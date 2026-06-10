# Claim and Eval Contract

## 1. Allowed Claims

| Claim | Required Evidence |
|---|---|
| The project implements a minimal agent strategy benchmark. | `AgentStrategy` interface, same `CaseSpec` across strategies, unit tests, sample run。 |
| Agent strategies can be compared under unified tasks. | Strategy leaderboard, per-family metrics, non-trivial success / cost differences。 |
| Tool use is exposed through an MCP-compatible boundary. | `ToolSpec`, `ToolRegistry`, `ToolExecutor`, structured tool traces; FastMCP adapter only if implemented。 |
| Context budget tradeoffs are measurable. | `context_chars_used`, `cost_proxy`, budget pressure cases, budget frontier report。 |
| A cost-aware control policy is demonstrated in bounded cases. | `context_budget_agent` value-of-information heuristic, success-cost frontier, dominated strategy analysis。 |
| Verification can reduce unsupported answers in bounded cases. | Verification-needed cases, `unsupported_answer_rate`, citation coverage, before/after strategy comparison。 |
| Reflection can recover some failures in bounded cases. | Reflective strategy retry trace, recovery cases, `reflection_recovery_rate`。 |
| Sensitive-action handling is demonstrated only as a small bounded task family. | PolicyDecision trace, allow/block/review cases, unsafe allow / false block metrics。 |

MVP public claims are limited to strategy benchmark, MCP-compatible in-process tool boundary, context budget tradeoffs, cost-aware control policy, and verification tradeoffs. Reflection, sensitive-action handling, FastMCP exposure, coding repair, and LLM-backed planning are claimable only after their traces, graders, metrics, and reports exist.

## 2. Label Visibility Contract

`gold`、`expected_outcome`、`grader`、`metadata.intended_split` 和 case-family 评测标签只能服务于评测与报告，不得进入被测策略或工具实现。

| Data | Grader | AgentStrategy | Tool Implementation | Report |
|---|---|---|---|---|
| `gold_doc_ids` / `expected_outcome` | 可读 | 禁止 | 禁止 | 可读 |
| `metadata.intended_split` | 可读 | 禁止 | 禁止 | 可读 |
| `family` / dimensions | 可读 | 禁止 | 禁止 | 可读 |
| `user_query` / `budget` | 可读 | 可读 | 按工具输入可读 | 可读 |
| `retrieval_doc_ids` per-case corpus pool | 可读 | 禁止 | 按工具输入可读 | 可读 |
| runtime provenance such as `source` / `trust_tier` | 可读 | 可读 | 可读 | 可读 |
| retrieved chunks / answer source ids | 可读 | 可读 | 可读 | 可读 |

Implementation rule: strategies receive `CaseView`, not full `CaseSpec`. Verification tools must validate grounding and source metadata from retrieved evidence; they must not receive gold labels such as `expected_doc_ids`.

## 3. Disallowed Claims

- Production-grade enterprise security。
- Full coding agent replacement。
- General RAG framework superiority。
- Human productivity improvement without real study evidence。
- Loomstead-style observability platform replacement。
- MCP-native runtime before an actual MCP adapter is implemented and demonstrated。
- LLM-backed strategy improvement before hosted/local planner experiments are implemented and measured。
- Algorithmic superiority beyond bounded cases and explicit baselines。

## 4. Minimum Metric Contract

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
| `success_conditioned_cost` | Average cost proxy among successful runs。 |
| `pareto_dominated_case_count` | Cases where a strategy is dominated by another strategy on success and cost。 |
| `unsafe_allow_rate` | Sensitive action allowed while required evidence is missing。 |
| `false_block_rate` | Benign or fully evidenced sensitive action blocked。 |

## 5. Case Card Contract

Each public case card must include:

- task and case family。
- strategy and budget。
- important tool calls。
- grader / verification result。
- success / failure。
- what the strategy comparison proves。
- honest limitation。

## 6. Review Gate

Before implementation sprint, at least one external/model review should challenge:

1. Whether the pivot away from Loomstead overlap is sufficient。
2. Whether the strategy set creates real ablation rather than labels。
3. Whether eval validity supports the claims。
4. Whether MCP-compatible is meaningful before FastMCP。
5. Whether the MVP fits one month without starving AlgoCoach。
6. Whether `context_budget_agent` is a real control policy rather than a throttling branch。
