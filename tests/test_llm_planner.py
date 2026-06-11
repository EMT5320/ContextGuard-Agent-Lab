"""Tests for cheap planner strategy and comparison behavior."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from contextguard_agent_lab.agents.kernel import AgentKernel
from contextguard_agent_lab.agents.planner import CheapLLMPlanner
from contextguard_agent_lab.agents.strategies import resolve_strategy
from contextguard_agent_lab.benchmark.loader import load_cases
from contextguard_agent_lab.benchmark.schema import BudgetSpec, CaseView
from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine
from contextguard_agent_lab.tools.factory import build_default_tool_executor


REPO_ROOT = Path(__file__).resolve().parents[1]


class LLMPlannerTest(unittest.TestCase):
    """Cheap planner strategy tests."""

    def test_planner_verification_rule_triggers_on_verify_case(self) -> None:
        """Verification-needed queries should request verify_citation."""

        case = CaseView(
            case_id="cg_verify_001",
            case_type="rag_qa",
            user_query="What must happen before verification-needed answers are accepted?",
            budget=BudgetSpec(max_tool_calls=4, max_context_chars=1600, max_verification_calls=1, cost_proxy_limit=7.0),
        )
        decision = CheapLLMPlanner().plan(case)
        self.assertTrue(decision.should_verify)
        self.assertGreaterEqual(decision.retrieval_top_k, 2)

    def test_llm_planner_differs_from_plan_execute_on_adversarial_case(self) -> None:
        """Cheap planner should keep shallow retrieval on adversarial queries."""

        cases = {case.case_id: case for case in load_cases(REPO_ROOT / "data/benchmark/cases.sample.jsonl")}
        policy = EvidencePolicyEngine.from_json(REPO_ROOT / "config" / "policies.json")
        kernel = AgentKernel(
            tools=build_default_tool_executor(REPO_ROOT, policy_engine=policy),
            policy_engine=policy,
        )
        adversarial = cases["cg_adv_001"]
        plan_execute = kernel.run(adversarial, strategy="plan_execute")
        llm_planner = kernel.run(adversarial, strategy="llm_planner")

        self.assertTrue(plan_execute.success)
        self.assertFalse(llm_planner.success)
        self.assertEqual(plan_execute.tool_calls[0].arguments["top_k"], 2)
        self.assertEqual(llm_planner.tool_calls[0].arguments["top_k"], 1)

    def test_resolve_strategy_accepts_llm_planner(self) -> None:
        """CLI strategy resolution should include llm_planner."""

        self.assertEqual(resolve_strategy("llm_planner").name, "llm_planner")


if __name__ == "__main__":
    unittest.main()
