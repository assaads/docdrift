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
    missing_docs: list[str] = field(default_factory=list)


@dataclass
class DriftReport:
    sources: list[SourceReport] = field(default_factory=list)

    def add(self, sr: SourceReport) -> None:
        self.sources.append(sr)

    def has_drift(self) -> bool:
        return any(sr.missing or sr.missing_docs for sr in self.sources)

    def render_summary(self) -> str:
        if not self.sources:
            return "docs-drift: WARNING — manifest has no sources (nothing to check)"
        lines: list[str] = []
        for sr in self.sources:
            if sr.missing_docs:
                lines.append(f"[{sr.name}] missing doc files: {sr.missing_docs}")
            if sr.missing:
                lines.append(f"[{sr.name}] docs {sr.docs} missing: {sr.missing}")
            if not sr.items and not sr.missing and not sr.missing_docs:
                lines.append(f"[{sr.name}] WARNING: extractor '{sr.extractor}' returned 0 items")
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
