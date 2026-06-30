"""Domain registry — maps domain names to environment instances."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import OverlayEnvironment

_registry: dict[str, "OverlayEnvironment"] = {}


def register_domain(name: str, env: "OverlayEnvironment") -> None:
    _registry[name] = env


def get_domain(name: str) -> "OverlayEnvironment | None":
    return _registry.get(name)


def get_registered_domains() -> list[str]:
    return list(_registry.keys())


def _bootstrap_domains() -> None:
    from .mpls import MPLSEnvironment

    register_domain("mpls", MPLSEnvironment())


_bootstrap_domains()
