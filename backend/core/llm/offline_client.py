"""Local-only JSON chat client.

The planner uses this module instead of cloud LLM SDKs. Ollama is the default
transport because it exposes a local HTTP API and supports JSON output.
"""
from __future__ import annotations

import json
import os
from typing import Protocol

import httpx


class OfflineLLM(Protocol):
    def chat_json(self, system: str, user: str, schema: dict | None = None) -> dict:
        ...


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None) -> None:
        self.base_url = (base_url or os.environ.get("OLLAMA_BASE_URL") or "http://localhost:11434").rstrip("/")
        self.model = model or os.environ.get("OVERLAY_LOCAL_MODEL") or "phi3:3.8b-mini-4k-instruct-q4_K_M"

    def chat_json(self, system: str, user: str, schema: dict | None = None) -> dict:
        payload = {
            "model": self.model,
            "format": "json",
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        response = httpx.post(f"{self.base_url}/api/chat", json=payload, timeout=60.0)
        response.raise_for_status()
        content = response.json()["message"]["content"]
        return json.loads(content)


def get_offline_llm() -> OfflineLLM:
    backend = os.environ.get("OVERLAY_LLM_BACKEND", "ollama").lower()
    if backend != "ollama":
        raise ValueError(f"Unsupported offline LLM backend: {backend}")
    return OllamaClient()
