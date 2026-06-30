from __future__ import annotations


def embed_text(text: str) -> list[float]:
    # Deterministic tiny fallback embedding for offline tests and demos.
    buckets = [0.0] * 16
    for idx, char in enumerate(text.encode("utf-8", errors="ignore")):
        buckets[idx % len(buckets)] += char / 255.0
    total = sum(buckets) or 1.0
    return [round(value / total, 6) for value in buckets]
