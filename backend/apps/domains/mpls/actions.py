"""MPLS action catalog used by PlannerAgent and the operator console."""
from __future__ import annotations

from typing import Any


MPLS_ACTIONS: list[dict[str, Any]] = [
    {
        "action_id": "reroute_lsp",
        "description": "Move an LSP to a lower-risk explicit path.",
        "parameters": {"lsp_id": "lsp-branch-a-dc", "new_path": ["ce-a", "pe1", "p2", "pe2", "dc"]},
        "reversibility": 0.9,
        "risk": 0.4,
        "requires_guardian": False,
        "relevant_states": ["degraded", "critical"],
    },
    {
        "action_id": "adjust_te_metric",
        "description": "Increase or decrease a Traffic Engineering metric on a link.",
        "parameters": {"link_id": "pe1-p1", "metric": 40},
        "reversibility": 0.95,
        "risk": 0.3,
        "requires_guardian": False,
        "relevant_states": ["degraded"],
    },
    {
        "action_id": "isolate_link",
        "description": "Temporarily remove a suspect link from forwarding.",
        "parameters": {"link_id": "p1-p2"},
        "reversibility": 0.6,
        "risk": 0.7,
        "requires_guardian": True,
        "relevant_states": ["critical"],
    },
    {
        "action_id": "drain_traffic",
        "description": "Drain traffic away from a router before maintenance or failure.",
        "parameters": {"node_id": "p1"},
        "reversibility": 0.7,
        "risk": 0.6,
        "requires_guardian": True,
        "relevant_states": ["degraded", "critical"],
    },
    {
        "action_id": "increase_bandwidth_reservation",
        "description": "Reserve more bandwidth for an RSVP-TE LSP.",
        "parameters": {"lsp_id": "lsp-branch-b-dc", "bw_mbps": 850},
        "reversibility": 0.95,
        "risk": 0.2,
        "requires_guardian": False,
        "relevant_states": ["recovering", "degraded"],
    },
    {
        "action_id": "failover_to_backup_lsp",
        "description": "Fail traffic over to the configured backup LSP.",
        "parameters": {"lsp_id": "lsp-branch-a-dc"},
        "reversibility": 0.5,
        "risk": 0.5,
        "requires_guardian": True,
        "relevant_states": ["critical"],
    },
    {
        "action_id": "restart_routing_process",
        "description": "Restart the routing process on a router.",
        "parameters": {"node_id": "p1"},
        "reversibility": 0.3,
        "risk": 0.9,
        "requires_guardian": True,
        "relevant_states": ["critical"],
    },
]


def action_by_id(action_id: str) -> dict[str, Any] | None:
    for action in MPLS_ACTIONS:
        if action["action_id"] == action_id:
            return action
    return None
