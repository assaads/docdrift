from __future__ import annotations

import argparse
import sys
from typing import Any

from docdrift.ctx import Context
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
        root = str(ctx.repo_root)
        if root not in sys.path:
            sys.path.insert(0, root)
        factory = source.factory
        module = factory.partition(":")[0]
        sys.modules.pop(module, None)  # fixtures share module name 'app' across stacks
        parser = ctx.importer(factory)()
        return _walk(parser)
