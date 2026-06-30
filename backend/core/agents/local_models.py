"""Local-only model registry for Overlay."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelEntry:
    key: str
    model_id: str
    display_name: str
    params_m: int
    size_mb: int
    task: str
    source: str
    description: str
    badge: str
    quantized: bool = True
    available: bool = True
    loaded: bool = False

    def as_dict(self) -> dict:
        return self.__dict__.copy()


_REGISTRY: dict[str, ModelEntry] = {
    "ollama-phi3": ModelEntry(
        key="ollama-phi3",
        model_id="phi3:3.8b-mini-4k-instruct-q4_K_M",
        display_name="Phi-3 Mini Q4",
        params_m=3800,
        size_mb=2300,
        task="chat-json",
        source="local",
        badge="Ollama",
        description="Default offline planner model for commodity NOC hardware.",
    ),
    "ollama-mistral": ModelEntry(
        key="ollama-mistral",
        model_id="mistral:7b-instruct-q4_K_M",
        display_name="Mistral 7B Q4",
        params_m=7000,
        size_mb=4400,
        task="chat-json",
        source="local",
        badge="Ollama",
        description="Higher-reasoning local model when VRAM allows.",
    ),
}


def get_model(key: str) -> ModelEntry:
    return _REGISTRY[key]


def registry_info() -> list[dict]:
    return [entry.as_dict() for entry in _REGISTRY.values()]
