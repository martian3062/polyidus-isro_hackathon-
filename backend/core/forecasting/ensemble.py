from __future__ import annotations


def weighted_forecast(series: list[list[float]], weights: list[float] | None = None) -> list[float]:
    if not series:
        return []
    weights = weights or [1.0 / len(series)] * len(series)
    horizon = min(len(row) for row in series)
    return [
        sum(row[i] * weight for row, weight in zip(series, weights, strict=False))
        for i in range(horizon)
    ]
