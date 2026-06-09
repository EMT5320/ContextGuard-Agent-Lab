# Architecture Skeleton

## 1. Layered Architecture

```text
Benchmark Layer
  CaseSpec / Corpus / BudgetSpec / ExpectedOutcome / GraderSpec

Agent Strategy Layer
  MVP: react_agent / plan_execute_agent / verify_then_answer_agent / context_budget_agent
  Full target: reflective_agent / optional llm_planner_agent / guarded_agent for sensitive family

Kernel and Execution Layer
  AgentState / AgentKernel / ToolAction / Observation / ToolExecutor / Grader

Tool Boundary Layer
  ToolSpec / ToolRegistry / ToolExecutor / Tool manifest / Retrieval tools / Verification tools / Sensitive tools / MCP adapters

Task Environment Layer
  Retrieval corpus / adversarial context / budget pressure / sensitive action / optional coding fixture

Trace and Eval Layer
  TraceEvent / ToolCallTrace / RunRecord / Metrics / Leaderboard / Reports / CaseCards
```

## 2. Core Data Flow

```text
CaseSpec
  -> AgentStrategy.plan()
  -> AgentKernel loop
  -> ToolExecutor.call(ToolSpec)
  -> Observation + budget update
  -> optional verification / reflection
  -> independent Grader
  -> RunRecord JSONL
  -> Metrics + Markdown report
```

Sensitive action policy decisions occur inside `ToolExecutor` only when a tool is marked as sensitive or side-effectful. They are not the main control path for all tasks.

## 3. Module Responsibilities

| Module | Responsibility | First Milestone |
|---|---|---|
| `benchmark/` | schemas, loaders, case validation, grader specs | CaseSpec + BudgetSpec + sample cases |
| `agents/` | strategy interface and implementations | 4 real strategies with different tool sequences |
| `tools/` | ToolSpec, registry, executor, manifest export, retrieval / verification tools | in-process tool boundary |
| `eval/` | independent grader, metrics, leaderboard | strategy-level summary |
| `trace/` | JSONL run records and timeline events | RunRecord writer / reader |
| `reports/` | Markdown report generation and case cards | ablation report |
| `mcp_server/` | FastMCP adapters | Full target after ToolSpec stabilizes |

## 4. Design Invariants

- Every strategy must run on the same `CaseSpec`.
- Strategy differences must show up in tool sequence, verification timing, reflection behavior, budget usage, or success outcome。
- Success scoring must be independent from the agent control loop。
- Tool calls must be structured and traceable。
- Tool manifest must expose schema, risk, cost, and MCP exposure metadata before MCP-compatible claims are emphasized。
- Budget consumption must be recorded per tool call。
- Reports must explain tradeoffs, not just rank strategies。

## 5. Stretch Boundaries

- FastMCP adapter enters after in-process ToolSpec / ToolExecutor are stable。
- Hosted LLM planning is optional until deterministic strategies produce meaningful ablation。
- Coding repair tasks enter only after retrieval / verification / budget cases produce a strong report。
- A2A is cut for the current portfolio sprint。
