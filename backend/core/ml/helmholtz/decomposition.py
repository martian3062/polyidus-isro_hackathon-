from __future__ import annotations

import numpy as np


def decompose_flow_field(incidence: np.ndarray, flows: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (advective, divergent) components using a graph Hodge sketch."""
    if incidence.size == 0 or flows.size == 0:
        return flows, flows

    divergence = incidence @ flows
    laplacian = incidence @ incidence.T
    potential = np.linalg.pinv(laplacian) @ divergence
    divergent = incidence.T @ potential
    advective = flows - divergent
    return advective, divergent
