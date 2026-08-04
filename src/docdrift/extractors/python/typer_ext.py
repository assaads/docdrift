from __future__ import annotations

import sys
from typing import Any

from docdrift.ctx import Context, ensure_importable
from docdrift.registry import register


@register("typer")
class TyperExtractor:
    name = "typer"

    def extract(self, source: Any, ctx: Context) -> set[str]:
        module = source.module
        ensure_importable(module, ctx.repo_root)
        sys.modules.pop(module, None)  # invalidate stale module cache (same name imported from a different root in a prior call)
        dotted = f"{module}:{getattr(source, 'app', 'app')}"
        app = ctx.importer(dotted)
        from typer.main import get_group

        return set(get_group(app).commands)
