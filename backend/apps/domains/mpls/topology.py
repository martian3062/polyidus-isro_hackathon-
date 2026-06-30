"""Small offline MPLS topology model for proposal and demo mode."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RouterNode:
    node_id: str
    label: str
    role: str
    site: str
    active_lsps: int = 0


@dataclass(frozen=True)
class MplsLink:
    source: str
    target: str
    link_id: str
    capacity_mbps: float
    utilization_pct: float
    latency_ms: float
    packet_loss_pct: float = 0.0


NODES: list[RouterNode] = [
    RouterNode("ce-a", "Branch A CE", "CE", "branch-a", 8),
    RouterNode("ce-b", "Branch B CE", "CE", "branch-b", 6),
    RouterNode("pe1", "Provider Edge 1", "PE", "provider", 34),
    RouterNode("pe2", "Provider Edge 2", "PE", "provider", 41),
    RouterNode("p1", "Core P1", "P", "provider-core", 72),
    RouterNode("p2", "Core P2", "P", "provider-core", 66),
    RouterNode("dc", "Datacenter CE", "CE", "datacenter", 14),
]

LINKS: list[MplsLink] = [
    MplsLink("ce-a", "pe1", "ce-a-pe1", 1000, 63, 8, 0.01),
    MplsLink("ce-b", "pe1", "ce-b-pe1", 1000, 71, 9, 0.02),
    MplsLink("pe1", "p1", "pe1-p1", 10000, 89, 14, 0.08),
    MplsLink("p1", "p2", "p1-p2", 10000, 94, 21, 0.18),
    MplsLink("p2", "pe2", "p2-pe2", 10000, 76, 13, 0.03),
    MplsLink("pe2", "dc", "pe2-dc", 2000, 67, 7, 0.01),
    MplsLink("pe1", "p2", "pe1-p2-backup", 10000, 42, 18, 0.02),
]

LSPS: list[dict[str, Any]] = [
    {
        "lsp_id": "lsp-branch-a-dc",
        "path": ["ce-a", "pe1", "p1", "p2", "pe2", "dc"],
        "backup_path": ["ce-a", "pe1", "p2", "pe2", "dc"],
        "reserved_mbps": 650,
        "state": "up",
    },
    {
        "lsp_id": "lsp-branch-b-dc",
        "path": ["ce-b", "pe1", "p1", "p2", "pe2", "dc"],
        "backup_path": ["ce-b", "pe1", "p2", "pe2", "dc"],
        "reserved_mbps": 520,
        "state": "up",
    },
]


def topology_snapshot() -> dict[str, Any]:
    return {
        "nodes": [node.__dict__ for node in NODES],
        "edges": [link.__dict__ for link in LINKS],
        "lsps": LSPS,
    }


def link_by_id(link_id: str) -> MplsLink | None:
    for link in LINKS:
        if link.link_id == link_id:
            return link
    return None
