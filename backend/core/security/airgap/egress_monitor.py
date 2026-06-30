from __future__ import annotations

import socket
import time
from dataclasses import dataclass

from core.agents.guardian import AuditSigner


FORBIDDEN_HOSTS = [
    "api.groq.com",
    "api.openai.com",
    "api.anthropic.com",
    "huggingface.co",
    "pinecone.io",
    "amazonaws.com",
]


@dataclass
class AirgapStatus:
    outbound_attempts: int
    blocked_hostnames: list[str]
    reachable_hostnames: list[str]
    verified_at: float
    policy: str
    auditor_signature: str


def probe_airgap(timeout: float = 0.75) -> AirgapStatus:
    reachable: list[str] = []
    blocked: list[str] = []
    for host in FORBIDDEN_HOSTS:
        try:
            ip = socket.gethostbyname(host)
            sock = socket.create_connection((ip, 443), timeout=timeout)
            sock.close()
            reachable.append(host)
        except OSError:
            blocked.append(host)

    payload = {
        "outbound_attempts": len(reachable),
        "blocked_hostnames": blocked,
        "reachable_hostnames": reachable,
        "verified_at": time.time(),
        "policy": "deny-all-egress",
    }
    return AirgapStatus(
        outbound_attempts=len(reachable),
        blocked_hostnames=blocked,
        reachable_hostnames=reachable,
        verified_at=payload["verified_at"],
        policy=payload["policy"],
        auditor_signature=AuditSigner().sign(payload),
    )
