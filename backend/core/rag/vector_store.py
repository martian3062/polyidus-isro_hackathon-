from __future__ import annotations


class LocalVectorStore:
    def __init__(self) -> None:
        self._rows: list[dict] = []

    def add(self, row: dict) -> None:
        self._rows.append(row)

    def query(self, query: str, k: int = 5) -> list[dict]:
        return self._rows[:k]
