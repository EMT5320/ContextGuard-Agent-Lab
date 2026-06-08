"""Tests for evidence-gated decisions."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from contextguard_agent_lab.guardrails.policy import EvidencePolicyEngine


class PolicyEngineTest(unittest.TestCase):
    """Policy engine unit tests."""

    def test_policy_blocks_missing_evidence(self) -> None:
        """Sensitive actions should be blocked when evidence is absent."""

        engine = EvidencePolicyEngine({"export_data": ["user_authorization", "data_scope"]})
        decision = engine.decide("case-1", "export_data", ["data_scope"])
        self.assertEqual(decision.decision, "block")
        self.assertEqual(decision.missing_evidence, ["user_authorization"])

    def test_policy_allows_complete_evidence(self) -> None:
        """Sensitive actions can proceed when all evidence is present."""

        engine = EvidencePolicyEngine({"export_data": ["user_authorization", "data_scope"]})
        decision = engine.decide("case-1", "export_data", ["data_scope", "user_authorization"])
        self.assertEqual(decision.decision, "allow")
        self.assertEqual(decision.missing_evidence, [])


if __name__ == "__main__":
    unittest.main()

