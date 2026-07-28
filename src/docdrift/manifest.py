"""The .docdrift.yml contract. No logic here — just the declarative schema.

A Source is intentionally open (extra="allow"): stack-specific fields
(`module`/`app` for typer, `obj` for click, `path`/`regex` for files, etc.)
are read by the matching extractor. Adding an extractor never changes this model.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Source(BaseModel):
    model_config = ConfigDict(extra="allow")
    extractor: str
    name: str | None = None
    docs: list[str] = Field(default_factory=list)   # empty => inherit Manifest.docs
    format: str = "{item}"                           # {item} = a surface element


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int = 1
    docs: list[str] = Field(default_factory=lambda: ["README.md"])
    sources: list[Source]
