from __future__ import annotations

from typing import Any

import numpy as np


def build_flow_field(topology: dict[str, Any], telemetry: dict[str, Any] | None = None) -> dict[str, Any]:
    nodes = topology.get("nodes", [])
    edges = topology.get("edges", [])
    node_ids = [n["node_id"] for n in nodes]
    node_index = {node_id: idx for idx, node_id in enumerate(node_ids)}
    incidence = np.zeros((len(node_ids), len(edges)), dtype=float)
    flows = np.zeros(len(edges), dtype=float)
    edge_ids: list[str] = []

    for col, edge in enumerate(edges):
        source = edge["source"]
        target = edge["target"]
        incidence[node_index[source], col] = -1.0
        incidence[node_index[target], col] = 1.0
        edge_ids.append(edge["link_id"])
        flows[col] = float(edge.get("capacity_mbps", 0.0)) * float(edge.get("utilization_pct", 0.0)) / 100.0

    return {
        "node_ids": node_ids,
        "edge_ids": edge_ids,
        "incidence": incidence,
        "flows": flows,
    }
