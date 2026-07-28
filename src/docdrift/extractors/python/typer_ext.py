from __future__ import annotations

import sys
from typing import Any

from docdrift.ctx import Context
from docdrift.registry import register


@register("typer")
class TyperExtractor:
    name = "typer"

    def extract(self, source: Any, ctx: Context) -> set[str]:
        root = str(ctx.repo_root)
        if root not in sys.path:
            sys.path.insert(0, root)
        module = source.module
        sys.modules.pop(module, None)  # fixtures share module name 'app' across stacks
        dotted = f"{module}:{getattr(source, 'app', 'app')}"
        app = ctx.importer(dotted)
        from typer.main import get_group

        return set(get_group(app).commands)
