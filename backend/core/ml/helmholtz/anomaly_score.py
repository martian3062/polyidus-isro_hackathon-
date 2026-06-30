from __future__ import annotations

import numpy as np


def divergence_magnitude_per_node(
    node_ids: list[str],
    incidence: np.ndarray,
    divergent_flows: np.ndarray,
) -> dict[str, float]:
    if incidence.size == 0 or divergent_flows.size == 0:
        return {node_id: 0.0 for node_id in node_ids}
    node_divergence = incidence @ divergent_flows
    max_mag = float(np.max(np.abs(node_divergence))) or 1.0
    return {
        node_id: round(abs(float(value)) / max_mag, 4)
        for node_id, value in zip(node_ids, node_divergence, strict=False)
    }
