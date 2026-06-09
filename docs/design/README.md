# Design Docs

> 状态：设计审稿期。本文是 ContextGuard Agent Lab 的设计导航页，目标是在大规模实现前锁定新版主轴：MCP-compatible Agent Strategy Benchmark。

## Current Design Set

1. `00_project_brief_2026-06-08.md`：项目简报与新版一句话定位。
2. `01_agent_kernel_design.md`：Agent strategy、kernel loop、ToolExecutor 和策略分化设计。
3. `02_eval_plan.md`：case families、metrics、reports 和 failure taxonomy。
4. `03_vision_and_positioning.md`：目标岗位、公开作品组合、差异化主张。
5. `04_architecture_skeleton.md`：架构层次、数据流和模块边界。
6. `05_claim_and_eval_contract.md`：公开 claim 与 required evidence。
7. `06_risk_register.md`：范围、重合、评测有效性和时间风险。
8. `07_roadmap_and_gates.md`：阶段门槛与实现顺序。
9. `08_background_snapshot.md`：脱敏背景、作品组合和目标岗位梯度。
10. `09_loomstead_overlap_and_pivot.md`：Loomstead 重合审计与 pivot 决策。
11. `10_execution_alignment_plan.md`：面向多 agent 并行开发的执行计划、阶段边界和防漂移约束。
12. `../review/02_round2_synthesis.md`：round2 多模型审稿吸收矩阵与最终执行顺序。

## Review Inputs

- `../review/00_multi_model_review_packet.md`：给其他模型的新版统一审稿包。
- `../review/01_reviewer_questionnaire.md`：结构化问题清单。
- `../review/02_round2_synthesis.md`：round2 讨论收束后的接受建议与 battle resolution。
- `../review/reviews/`：历史 review。注意：其中一部分基于旧版 `evidence-governed` 方案，不应视为当前最终方案。

## Current Spine

```text
AgentStrategy + ToolSpec/ToolExecutor + MCP-compatible boundary + cost-aware context budget + strategy ablation + Markdown reports
```

RAG、adversarial context、sensitive action 和 coding fixture 都是任务环境，不是项目本体。
