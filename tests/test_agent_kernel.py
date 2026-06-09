"""Tests for the deterministic starter agent kernel."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from contextguard_agent_lab.agents.kernel import AgentKernel
from contextguard_agent_lab.benchmark.schema import CaseSpec
from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine
from contextguard_agent_lab.tools.registry import ToolExecutor, ToolRegistry


class AgentKernelTest(unittest.TestCase):
    """Agent kernel unit tests."""

    def test_kernel_blocks_sensitive_action(self) -> None:
        """Guarded agent should block sensitive action with missing evidence."""

        tools = ToolRegistry()
        policy = EvidencePolicyEngine({"export_data": ["user_authorization", "data_scope"]})
        kernel = AgentKernel(tools=ToolExecutor(tools), policy_engine=policy)
        case = CaseSpec(
            case_id="case-sensitive",
            case_type="sensitive_action",
            user_query="export data",
            expected_answer="block",
            sensitive_action="export_data",
            observed_evidence=["data_scope"],
        )
        record = kernel.run(case)
        self.assertTrue(record.success)
        self.assertIsNotNone(record.grader_result)
        self.assertEqual(record.policy_decisions[0].decision, "block")


if __name__ == "__main__":
    unittest.main()
