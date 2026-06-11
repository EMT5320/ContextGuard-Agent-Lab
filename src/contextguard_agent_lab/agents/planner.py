"""Cheap planner backends for LLM-backed strategy comparison."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from contextguard_agent_lab.benchmark.schema import CaseView


@dataclass(slots=True)
class PlannerDecision:
    """Structured planner output consumed by llm_planner strategy."""

    plan: list[str]
    retrieval_top_k: int
    should_verify: bool
    should_retry_after_verification: bool
    planner_backend: str
    planner_reason: str


class CheapLLMPlanner:
    """Offline cheap planner used for reproducible deterministic-vs-LLM comparison.

    The default backend is a keyword policy stand-in that returns JSON-shaped
    decisions without calling a hosted model. Set CONTEXTGUARD_PLANNER_BACKEND=http
    to route prompts to an OpenAI-compatible endpoint.
    """

    def __init__(self, policy_path: str | Path | None = None) -> None:
        root = Path(__file__).resolve().parents[3]
        self.policy_path = Path(policy_path) if policy_path is not None else root / "data" / "planner" / "cheap_planner_policy.json"
        self.policy = self._load_policy(self.policy_path)
        self.backend = os.environ.get("CONTEXTGUARD_PLANNER_BACKEND", "keyword").strip().lower()

    def plan(self, case: CaseView) -> PlannerDecision:
        """Return a planner decision for one runtime-visible case view."""

        if self.backend == "http":
            return self._plan_via_http(case)
        return self._plan_via_keyword_policy(case)

    def _plan_via_keyword_policy(self, case: CaseView) -> PlannerDecision:
        """Apply the offline keyword policy that mimics cheap planner JSON output."""

        query = case.user_query.lower()
        tokens = set(re.findall(r"[a-z0-9_]+", query))
        decision = dict(self.policy.get("default", {}))
        reason = "default_policy"

        for rule in self.policy.get("rules", []):
            if self._rule_matches(rule, tokens, query):
                decision.update({key: value for key, value in rule.items() if key.startswith(("top_k", "should_", "plan"))})
                reason = str(rule.get("reason", "matched_rule"))
                break

        top_k = max(1, int(decision.get("top_k", 1)))
        should_verify = bool(decision.get("should_verify", False)) and case.budget.max_verification_calls > 0
        should_retry = bool(decision.get("should_retry_after_verification", False))
        plan_steps = [str(step) for step in decision.get("plan", ["llm_planner: draft steps", "execute plan"])]
        return PlannerDecision(
            plan=plan_steps,
            retrieval_top_k=top_k,
            should_verify=should_verify,
            should_retry_after_verification=should_retry,
            planner_backend="keyword",
            planner_reason=reason,
        )

    def _plan_via_http(self, case: CaseView) -> PlannerDecision:
        """Optional hosted planner path for owners with an OpenAI-compatible endpoint."""

        try:
            import urllib.error
            import urllib.request
        except ImportError as exc:  # pragma: no cover - stdlib should always exist
            raise RuntimeError("urllib is required for http planner backend") from exc

        endpoint = os.environ.get("CONTEXTGUARD_PLANNER_URL", "").strip()
        if not endpoint:
            raise RuntimeError("CONTEXTGUARD_PLANNER_URL is required when CONTEXTGUARD_PLANNER_BACKEND=http")

        prompt = (
            "Return JSON with keys plan (string list), retrieval_top_k (int), "
            "should_verify (bool), should_retry_after_verification (bool). "
            f"Case query: {case.user_query}"
        )
        payload = json.dumps(
            {
                "model": os.environ.get("CONTEXTGUARD_PLANNER_MODEL", "cheap-planner"),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ.get('CONTEXTGUARD_PLANNER_API_KEY', '')}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"hosted planner request failed: {exc}") from exc

        content = body.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        parsed = json.loads(content)
        return PlannerDecision(
            plan=[str(step) for step in parsed.get("plan", ["llm_planner: hosted plan"])],
            retrieval_top_k=max(1, int(parsed.get("retrieval_top_k", 1))),
            should_verify=bool(parsed.get("should_verify", False)) and case.budget.max_verification_calls > 0,
            should_retry_after_verification=bool(parsed.get("should_retry_after_verification", False)),
            planner_backend="http",
            planner_reason="hosted_response",
        )

    @staticmethod
    def _load_policy(path: Path) -> dict[str, Any]:
        """Load the offline keyword planner policy."""

        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _rule_matches(rule: dict[str, Any], tokens: set[str], query: str) -> bool:
        """Return whether one policy rule matches the query."""

        contains_all = [str(item).lower() for item in rule.get("query_contains_all", [])]
        if contains_all and not set(contains_all).issubset(tokens):
            return False
        contains_any = [str(item).lower() for item in rule.get("query_contains_any", [])]
        if contains_any and not any(item in tokens or item in query for item in contains_any):
            return False
        regex = rule.get("query_regex")
        if regex and not re.search(str(regex), query):
            return False
        return bool(contains_all or contains_any or regex)
