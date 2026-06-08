"""Evidence-gated policy engine."""

from __future__ import annotations

import json
from pathlib import Path

from contextguard_agent_lab.benchmark.schema import PolicyDecision


class EvidencePolicyEngine:
    """Decide whether sensitive actions have sufficient evidence."""

    def __init__(self, requirements: dict[str, list[str]], default_decision: str = "block") -> None:
        self.requirements = requirements
        self.default_decision = default_decision

    @classmethod
    def from_json(cls, path: str | Path) -> "EvidencePolicyEngine":
        """Load policy requirements from a small JSON file."""

        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            requirements=data.get("sensitive_actions", {}),
            default_decision=data.get("default_decision", "block"),
        )

    def decide(self, case_id: str, action: str, observed_evidence: list[str]) -> PolicyDecision:
        """Return allow/block/review based on missing evidence."""

        required = self.requirements.get(action, [])
        observed = sorted(set(observed_evidence))
        missing = [item for item in required if item not in observed]
        if missing:
            reason = "missing evidence: " + ", ".join(missing)
            decision = self.default_decision
        else:
            reason = "all required evidence present"
            decision = "allow"
        return PolicyDecision(
            case_id=case_id,
            action=action,
            decision=decision,  # type: ignore[arg-type]
            required_evidence=required,
            observed_evidence=observed,
            missing_evidence=missing,
            reason=reason,
        )
