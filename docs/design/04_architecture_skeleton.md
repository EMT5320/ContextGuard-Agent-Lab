# Architecture Skeleton

## 1. Layered architecture

```text
Benchmark Layer
  CaseSpec / Corpus / WorkspaceFixture / PolicyFixture

Agent Strategy Layer
  react_agent / plan_execute_agent / reflective_agent / guarded_agent / context_budget_agent

Agent Kernel Layer
  AgentState / Planner / ToolExecutor / Observation / Reflection / RepairLoop

Tool Boundary Layer
  Retrieval tools / Workspace tools / Sensitive tools / MCP adapters

Governance Layer
  EvidencePolicyEngine / InjectionCheck / PermissionProfile / HumanReviewStub

Trace & Eval Layer
  ToolCallTrace / PolicyDecision / RunRecord / Metrics / Reports / CaseCards
```

## 2. Core data flow

```text
CaseSpec
  -> AgentState
  -> strategy.plan()
  -> ToolRegistry.call()
  -> Observation
  -> PolicyDecision when needed
  -> Reflection / Repair when failed
  -> RunRecord JSONL
  -> Metrics + Markdown report
```

## 3. Module responsibilities

| Module | Responsibility | First milestone |
|---|---|---|
| `benchmark/` | schemas, loaders, case validation | CaseSpec + sample cases |
| `agents/` | kernel and strategy implementations | deterministic starter strategies |
| `tools/` | in-process tools and MCP-compatible signatures | retrieval + workspace + sensitive stubs |
| `guardrails/` | evidence gate and injection checks | EvidencePolicyEngine |
| `trace/` | JSONL trace and case replay | RunRecord writer/reader |
| `eval/` | metrics and leaderboard | task success + tool count + safety |
| `mcp_server/` | FastMCP adapters | W2 integration |

## 4. Design invariants

- Tool calls must be structured and traceable.
- Sensitive actions must pass through policy decision records.
- Every strategy must run on the same CaseSpec.
- Every report must link back to trace artifacts.
- Code repair tasks must run in bounded fixture workspaces.

## 5. Stretch boundaries

- A2A is a reviewer handoff demo only.
- Hosted LLM planning is optional until deterministic strategy baselines are stable.
- Real open-source repo repair tasks enter only after fixture tasks are reliable.
