from __future__ import annotations


RUNBOOK_CHUNKS = [
    {
        "citation_id": "RB-009",
        "source": "offline_runbook/congestion_preempt.md",
        "text": "For RSVP-TE congestion, prefer reversible LSP reroute before link isolation.",
        "vendor": "generic",
        "doc_type": "runbook",
    },
    {
        "citation_id": "RFC-3209",
        "source": "rfc3209",
        "text": "RSVP-TE establishes explicit LSPs and supports resource reservation for traffic engineering.",
        "vendor": "ietf",
        "doc_type": "rfc",
    },
]


def retrieve(query: str, k: int = 5, filters: dict | None = None) -> list[dict]:
    q = query.lower()
    scored = []
    for chunk in RUNBOOK_CHUNKS:
        score = sum(1 for token in q.split() if token in chunk["text"].lower())
        scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:k]]
