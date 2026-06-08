# Agent Kernel Design

## 1. Kernel loop

```text
CaseSpec -> AgentState -> plan -> tool call -> observation -> policy decision -> reflection/repair -> RunRecord
```

## 2. Core objects

- `CaseSpec`：统一任务定义。
- `AgentState`：当前任务状态、计划、观察、证据和错误。
- `ToolRegistry`：工具注册与调用边界。
- `PolicyEngine`：敏感动作证据校验。
- `TraceRecorder`：记录 tool call、policy decision 和 final answer。
- `RunRecord`：单 case 结果。

## 3. Strategy comparison

| Strategy | Purpose |
|---|---|
| `react_agent` | 最小 observe-act baseline。 |
| `plan_execute_agent` | 显式计划，便于审计。 |
| `reflective_agent` | 失败后进行一次修复。 |
| `guarded_agent` | 敏感动作前执行 evidence gate。 |
| `context_budget_agent` | 评估上下文预算与收益。 |

## 4. Safety model

本项目采用 bounded evidence contract：

```text
action = export_data
required_evidence = [user_authorization, data_scope, policy_allowance]
observed_evidence = [data_scope]
decision = block
```

该机制只用于公开工程展示，不声明企业级安全能力。
