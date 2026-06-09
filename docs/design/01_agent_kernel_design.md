# Agent Kernel Design

## 1. Kernel Loop

新版 kernel 的目标不是复刻完整 coding agent，而是让多个策略在同一批 `CaseSpec` 上产生可解释、可度量的行为差异。

```text
CaseSpec
  -> AgentState
  -> AgentStrategy.plan()
  -> AgentStrategy.next_action()
  -> ToolExecutor.call(ToolSpec, arguments)
  -> Observation
  -> optional verification / reflection
  -> independent grader
  -> RunRecord + metrics
```

## 2. Core Objects

- `CaseSpec`：统一任务定义，包含 task family、expected outcome、budget、grader type。
- `AgentState`：当前计划、观察、检索证据、工具调用、预算消耗和失败原因。
- `AgentStrategy`：决定下一步动作的策略接口。
- `ToolSpec`：工具名称、schema、risk level、side effect、cost estimate、MCP exposure metadata。
- `ToolExecutor`：执行工具、计量 latency / cost / context chars，并统一写 trace。
- `Grader`：独立判定 success / unsupported answer / citation coverage / budget violation。
- `RunRecord`：单 case × 单 strategy 的最终结果。

## 3. Strategy Interface

```python
class AgentStrategy(Protocol):
    name: str

    def plan(self, state: AgentState) -> list[str]: ...
    def next_action(self, state: AgentState) -> ToolAction | FinalAnswer: ...
    def observe(self, state: AgentState, observation: Observation) -> None: ...
    def should_reflect(self, state: AgentState) -> bool: ...
```

策略必须改变控制流、工具序列、验证时机或预算行为。只改变 plan 文本不算真实策略差异。

## 4. Starter Strategies

| Strategy | Purpose | Expected Difference |
|---|---|---|
| `react_agent` | 最小直接行动 baseline | 工具少，失败率较高，容易 unsupported answer。 |
| `plan_execute_agent` | 先分解再执行 | 工具调用更多，multi-hop retrieval 更稳。 |
| `verify_then_answer_agent` | 先验证 citation / support 再回答 | unsupported answer 更少，成本更高。 |
| `reflective_agent` | 失败后一次 retry | repair / recovery 更强，latency 与工具调用更高。 |
| `context_budget_agent` | 在预算内选择 retrieval / verification | cost_proxy 更低，可能牺牲成功率。 |

`guarded_agent` 保留为 sensitive action 小环境的策略，不再作为主线策略。

## 5. Safety and Policy Boundary

Sensitive action 仍使用 bounded evidence contract，但它只是一个 case family：

```text
action = export_data
required_evidence = [user_authorization, data_scope, policy_allowance]
observed_evidence = [data_scope]
decision = block
```

该机制用于展示 tool execution boundary 的可扩展性，不声明企业级安全能力，也不作为 ContextGuard 的核心差异化。
