"""MPLS telemetry normalization."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MplsSignal:
    source: str
    features: dict[str, float]
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_link_telemetry(link: Any, tick: int) -> MplsSignal:
    flap_burst = 3.0 if link.link_id == "p1-p2" and tick % 9 in (0, 1) else 0.0
    jitter = max(1.0, link.latency_ms * 0.13 + (tick % 4))
    return MplsSignal(
        source=link.link_id,
        features={
            "interface_util": min(100.0, link.utilization_pct + ((tick % 5) - 2) * 1.8),
            "latency_ms": link.latency_ms + (tick % 3) * 1.2,
            "jitter_ms": jitter,
            "packet_loss": link.packet_loss_pct,
            "bgp_adj_changes_per_min": flap_burst,
            "lsp_rsvp_state": 1.0,
            "netflow_mbps": link.capacity_mbps * link.utilization_pct / 100.0,
        },
        metadata={"link_id": link.link_id, "tick": tick},
    )
