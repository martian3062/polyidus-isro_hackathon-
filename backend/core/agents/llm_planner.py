"""Offline LLM planner for Overlay.

This keeps PlannerAgent's Tier 2 and Tier 3 fallbacks unchanged, but replaces
the old cloud LLM transport with a local Ollama JSON-mode call.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from typing import Any

from .perceiver import PerceptionResult
from .planner import ActionPlan, PlannerAgent

logger = logging.getLogger("overlay.llm_planner")

_SYSTEM_PROMPT = """\
You are an autonomous action planner for the Overlay air-gapped MPLS
operations swarm. You will receive a structured perception result and a list
of available MPLS actions. Choose the single best action and explain it.

Rules:
- Return ONLY valid JSON, no prose outside the JSON object.
- Be concise in rationale.
- confidence and expected_reward must be between 0.0 and 1.0.
- If risk_score > 0.7, set requires_guardian_approval to true.
- Prefer reversible MPLS actions before destructive changes.
"""

_USER_TEMPLATE = """\
Domain: {domain}
State: {state_label} (confidence={confidence:.2f}, risk_score={risk_score:.2f})
Features: {features}
Available actions: {actions}

Return JSON with exactly these fields:
{{
  "action_id": "<chosen action_id from the list above>",
  "rationale": "<1-2 sentence explanation>",
  "confidence": <float>,
  "expected_reward": <float>,
  "requires_guardian_approval": <bool>
}}
"""


class LLMPlannerAgent(PlannerAgent):
    """PlannerAgent with a local LLM-backed Tier 1."""

    def __init__(
        self,
        agent_id: str | None = None,
        domain: str = "generic",
        model: str = "phi3:3.8b-mini-4k-instruct-q4_K_M",
    ):
        super().__init__(agent_id, domain)
        self._model = model
        self._offline_client = None

    def _get_client(self):
        if self._offline_client is None:
            try:
                from core.llm.offline_client import OllamaClient

                self._offline_client = OllamaClient(
                    model=os.environ.get("OVERLAY_LOCAL_MODEL", self._model)
                )
            except Exception as exc:
                logger.warning("Offline LLM client unavailable: %s", exc)
        return self._offline_client

    def _plan_tier1(self, context: PerceptionResult) -> ActionPlan:
        client = self._get_client()
        if client is None:
            raise NotImplementedError("Offline LLM unavailable - falling back to tier2")

        action_ids = [a["action_id"] for a in self._domain_actions] or ["noop"]
        user_msg = _USER_TEMPLATE.format(
            domain=context.domain,
            state_label=context.state_label,
            confidence=context.confidence,
            risk_score=context.risk_score,
            features=json.dumps(context.features, default=str),
            actions=action_ids,
        )

        try:
            data: dict[str, Any] = client.chat_json(_SYSTEM_PROMPT, user_msg, schema={})
        except Exception as exc:
            logger.warning("Offline LLM tier1 call failed: %s", exc)
            raise NotImplementedError(f"Offline LLM call failed: {exc}") from exc

        action_id = data.get("action_id", "noop")
        valid_ids = {a["action_id"] for a in self._domain_actions}
        if action_id not in valid_ids:
            logger.warning("LLM returned unknown action '%s', defaulting to noop", action_id)
            action_id = next(iter(valid_ids), "noop")

        arm = self._arms.get(action_id)
        params = arm.action_params if arm else {}

        return ActionPlan(
            plan_id=str(uuid.uuid4())[:8],
            domain=context.domain,
            actions=[{"action_id": action_id, "parameters": params}],
            rationale=data.get("rationale", "Offline LLM decision"),
            confidence=float(data.get("confidence", context.confidence)),
            expected_reward=float(data.get("expected_reward", 0.7)),
            tier_used="tier1_offline_llm",
            requires_guardian_approval=bool(
                data.get("requires_guardian_approval", context.risk_score > 0.7)
            ),
        )
