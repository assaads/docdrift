from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class SourceReport:
    name: str
    extractor: str
    items: list[str]
    literals: list[str]
    missing: list[str]
    docs: list[str]


@dataclass
class DriftReport:
    sources: list[SourceReport] = field(default_factory=list)

    def add(self, sr: SourceReport) -> None:
        self.sources.append(sr)

    def has_drift(self) -> bool:
        return any(sr.missing for sr in self.sources)

    def render_summary(self) -> str:
        lines = []
        for sr in self.sources:
            if sr.missing:
                lines.append(
                    f"[{sr.name}] docs {sr.docs} missing: {sr.missing}"
                )
        if not lines:
            return "docs-drift: OK (no drift)"
        return "docs-drift: DRIFT DETECTED\n" + "\n".join(lines)

    def render(self, as_json: bool = False) -> str:
        if as_json:
            return json.dumps(
                {"has_drift": self.has_drift(),
                 "sources": [sr.__dict__ for sr in self.sources]},
                indent=2,
            )
        return self.render_summary()
