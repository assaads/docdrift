from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Extractor(Protocol):
    name: str

    def extract(self, source: Any, ctx: Any) -> set[str]: ...
