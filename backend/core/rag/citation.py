from __future__ import annotations


def has_citation(text: str) -> bool:
    return "[" in text and "]" in text
