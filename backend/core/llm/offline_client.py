"""JSON chat clients for Overlay planner decisions.

Ollama remains the default air-gapped transport. Groq can be enabled for hosted
demo runs by setting OVERLAY_LLM_BACKEND=groq and GROQ_API_KEY.
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


class GroqClient:
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.base_url = (
            base_url
            or os.environ.get("GROQ_BASE_URL")
            or "https://api.groq.com/openai/v1"
        ).rstrip("/")
        self.model = model or os.environ.get("GROQ_MODEL") or "llama-3.3-70b-versatile"
        self.api_key = api_key or os.environ.get("GROQ_API_KEY") or ""
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required when OVERLAY_LLM_BACKEND=groq")

    def chat_json(self, system: str, user: str, schema: dict | None = None) -> dict:
        payload = {
            "model": self.model,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=60.0,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)


def get_offline_llm() -> OfflineLLM:
    backend = os.environ.get("OVERLAY_LLM_BACKEND", "ollama").lower()
    if backend == "ollama":
        return OllamaClient()
    if backend == "groq":
        return GroqClient()
    raise ValueError(f"Unsupported LLM backend: {backend}")
