from __future__ import annotations

import sys
from typing import Any

from docdrift.ctx import Context
from docdrift.registry import register


@register("click")
class ClickExtractor:
    name = "click"

    def extract(self, source: Any, ctx: Context) -> set[str]:
        root = str(ctx.repo_root)
        if root not in sys.path:
            sys.path.insert(0, root)
        target = source.obj
        module = target.partition(":")[0]
        sys.modules.pop(module, None)  # invalidate stale module cache (same name imported from a different root in a prior call)
        group = ctx.importer(target)
        names: set[str] = set(group.commands)
        for sub in getattr(group, "list_groups", lambda: [])():
            names |= set(sub.commands)
        return names
