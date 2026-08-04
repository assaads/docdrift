from __future__ import annotations

import sys
from typing import Any

from docdrift.ctx import Context, ensure_importable
from docdrift.registry import register


@register("click")
class ClickExtractor:
    name = "click"

    def extract(self, source: Any, ctx: Context) -> set[str]:
        target = source.obj
        module = target.partition(":")[0]
        ensure_importable(module, ctx.repo_root)
        sys.modules.pop(module, None)  # invalidate stale module cache (same name imported from a different root in a prior call)
        group = ctx.importer(target)
        names: set[str] = set(group.commands)
        for sub in getattr(group, "list_groups", lambda: [])():
            names |= set(sub.commands)
        return names
