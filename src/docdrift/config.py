from __future__ import annotations

from pathlib import Path

import yaml

from docdrift.manifest import Manifest


class DocdriftConfigError(ValueError):
    """Raised when the manifest is missing, malformed, or the wrong version."""


def load(path: Path) -> Manifest:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise DocdriftConfigError(
            f"manifest must be a mapping, got {type(raw).__name__}"
        )
    if raw.get("version") != 1:
        raise DocdriftConfigError(
            f"unsupported/missing manifest version: {raw.get('version')!r} "
            "(expected version: 1)"
        )
    return Manifest.model_validate(raw)


def load_first(paths: list[Path]) -> Manifest:
    for p in paths:
        if Path(p).exists():
            return load(Path(p))
    raise FileNotFoundError(f"no docdrift config found in: {paths}")
