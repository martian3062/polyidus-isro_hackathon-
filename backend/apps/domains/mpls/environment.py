"""Overlay MPLS/SD-WAN domain adapter."""
from __future__ import annotations

import itertools
import time
from typing import Iterator

from apps.domains.base import ActionOutcome, DomainAction, OverlayEnvironment, RawSignal

from .actions import MPLS_ACTIONS, action_by_id
from .signals import normalize_link_telemetry
from .topology import LINKS, topology_snapshot


class MPLSEnvironment(OverlayEnvironment):
    domain_name = "mpls"

    def __init__(self) -> None:
        self._tick = 0
        self._last_action: dict | None = None

    def signal_stream(self) -> Iterator[RawSignal]:
        for tick in itertools.count(self._tick):
            self._tick = tick + 1
            for link in LINKS:
                signal = normalize_link_telemetry(link, tick)
                yield RawSignal(
                    timestamp=time.time(),
                    domain=self.domain_name,
                    source=signal.source,
                    features=signal.features,
                    metadata=signal.metadata,
                )

    def execute_action(self, action: DomainAction) -> ActionOutcome:
        spec = action_by_id(action.type) or action_by_id(action.action_id)
        if spec is None:
            return ActionOutcome(
                action_id=action.action_id,
                success=False,
                reward=0.0,
                error=f"unknown MPLS action: {action.type or action.action_id}",
            )

        risk = float(spec.get("risk", 0.5))
        reversibility = float(spec.get("reversibility", 0.5))
        reward = max(0.0, min(1.0, (1.0 - risk) * 0.6 + reversibility * 0.4))
        self._last_action = {"action": spec["action_id"], "parameters": action.parameters}
        return ActionOutcome(
            action_id=action.action_id,
            success=True,
            reward=reward,
            state_delta={"last_action": self._last_action},
            latency_ms=42.0,
        )

    def reward(self, outcome: ActionOutcome) -> float:
        return max(0.0, min(1.0, outcome.reward))

    def available_actions(self) -> list[dict]:
        return MPLS_ACTIONS

    def bootstrap_graph(self) -> list[dict]:
        return topology_snapshot()["nodes"]

    def topology(self) -> dict:
        return topology_snapshot()

    def flow_divergence(self) -> dict:
        from core.ml.helmholtz.network_flow_field import build_flow_field
        from core.ml.helmholtz.decomposition import decompose_flow_field
        from core.ml.helmholtz.anomaly_score import divergence_magnitude_per_node

        topo = topology_snapshot()
        flow = build_flow_field(topo, {})
        _, divergent = decompose_flow_field(flow["incidence"], flow["flows"])
        return {
            "nodes": divergence_magnitude_per_node(flow["node_ids"], flow["incidence"], divergent),
            "edges": flow["edge_ids"],
        }

    def forecasts(self) -> list[dict]:
        from core.forecasting.time_to_impact import estimate_time_to_breach

        rows: list[dict] = []
        for link in LINKS:
            forecast = [min(100.0, link.utilization_pct + i * (2.1 if link.link_id == "p1-p2" else 0.6)) for i in range(1, 11)]
            estimate = estimate_time_to_breach(forecast, threshold=95.0, step_seconds=30)
            rows.append({
                "target_metric": f"link_util_{link.link_id}",
                "horizon_seconds": 300,
                "forecast": forecast,
                "confidence_band_low": [max(0.0, v - 5.0) for v in forecast],
                "confidence_band_high": [min(100.0, v + 5.0) for v in forecast],
                "time_to_breach_seconds": estimate.time_to_breach_seconds,
                "breach_threshold": 95.0,
                "forecast_confidence": estimate.confidence,
                "fallback_to_persistence": False,
            })
        return rows

    def telemetry_snapshot(self, window_seconds: int = 300) -> dict:
        return {
            "window_seconds": window_seconds,
            "topology": topology_snapshot(),
            "signals": [
                {
                    "source": normalize_link_telemetry(link, self._tick).source,
                    "features": normalize_link_telemetry(link, self._tick).features,
                }
                for link in LINKS
            ],
        }

    def inject_fault(self, scenario_id: str) -> dict:
        known = {
            "progressive_congestion": "p1-p2 utilization rising toward 95%",
            "bgp_flap_cascade": "BGP adjacency churn injected near pe1",
            "mpls_underlay_intermittent": "Packet loss spikes on p1-p2",
            "controller_policy_drift": "TE metric drift on pe1-p1",
        }
        return {
            "scenario_id": scenario_id,
            "accepted": scenario_id in known,
            "detail": known.get(scenario_id, "unknown scenario"),
        }

    def health_check(self) -> dict:
        return {
            "domain": self.domain_name,
            "status": "ok",
            "mode": "offline-simulated",
            "routers": len(topology_snapshot()["nodes"]),
            "links": len(topology_snapshot()["edges"]),
            "lsps": len(topology_snapshot()["lsps"]),
            "last_action": self._last_action,
        }
