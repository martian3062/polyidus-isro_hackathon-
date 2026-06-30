from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BreachEstimate:
    time_to_breach_seconds: int | None
    confidence: float


def estimate_time_to_breach(
    forecast: list[float],
    threshold: float,
    step_seconds: int,
) -> BreachEstimate:
    for idx, value in enumerate(forecast, start=1):
        if value >= threshold:
            distance = max(0.0, min(1.0, (value - threshold) / max(threshold, 1.0)))
            return BreachEstimate(idx * step_seconds, min(0.95, 0.72 + distance))
    return BreachEstimate(None, 0.62)
