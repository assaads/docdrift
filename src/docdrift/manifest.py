"""The .docdrift.yml contract. No logic here — just the declarative schema.

A Source is intentionally open (extra="allow"): stack-specific fields
(`module`/`app` for typer, `obj` for click, `path`/`regex` for files, etc.)
are read by the matching extractor. Adding an extractor never changes this model.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Source(BaseModel):
    model_config = ConfigDict(extra="allow")
    extractor: str
    name: str | None = None
    docs: list[str] = Field(default_factory=list)   # empty => inherit Manifest.docs
    format: str = "{item}"                           # {item} = a surface element

    @field_validator("format")
    @classmethod
    def _format_must_reference_item(cls, v: str) -> str:
        if "{item}" not in v:
            raise ValueError("format must contain '{item}' (the surface element placeholder)")
        return v


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int = 1
    docs: list[str] = Field(default_factory=lambda: ["README.md"])
    sources: list[Source]
