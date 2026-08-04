from __future__ import annotations

import argparse
import sys
from typing import Any

from docdrift.ctx import Context, ensure_importable
from docdrift.registry import register


def _walk(parser: argparse.ArgumentParser) -> set[str]:
    names: set[str] = set()
    for action in parser._actions:  # noqa: SLF001 (stable introspection API)
        if isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
            for nm, sub in action.choices.items():
                names.add(nm)
                names |= _walk(sub)
    return names


@register("argparse")
class ArgparseExtractor:
    name = "argparse"

    def extract(self, source: Any, ctx: Context) -> set[str]:
        factory = source.factory
        module = factory.partition(":")[0]
        ensure_importable(module, ctx.repo_root)
        sys.modules.pop(module, None)  # invalidate stale module cache (same name imported from a different root in a prior call)
        parser = ctx.importer(factory)()
        return _walk(parser)
