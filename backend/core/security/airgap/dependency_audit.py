from __future__ import annotations

from pathlib import Path


CLOUD_CLIENT_MARKERS = ("groq", "openai", "anthropic", "pinecone")


def scan_requirements(requirements_path: str | Path) -> dict:
    path = Path(requirements_path)
    if not path.exists():
        return {"path": str(path), "findings": []}
    findings = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        normalized = line.strip().lower()
        if normalized and not normalized.startswith("#"):
            for marker in CLOUD_CLIENT_MARKERS:
                if normalized.startswith(marker):
                    findings.append({"line": line_no, "package": normalized, "marker": marker})
    return {"path": str(path), "findings": findings}
