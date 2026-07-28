from __future__ import annotations

import importlib
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _import(dotted: str) -> Any:
    """Import 'pkg.mod' or 'pkg.mod:attr' (attr may be dotted)."""
    mod_part, _, attr = dotted.partition(":")
    obj: Any = importlib.import_module(mod_part)
    for a in attr.split(".") if attr else []:
        obj = getattr(obj, a)
    return obj


def _run(argv: list[str], env: dict[str, str] | None = None,
         cwd: Path | None = None) -> str:
    """Run a command, return ANSI-stripped stdout (never raises on non-zero)."""
    res = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=cwd, check=False)
    return _ANSI.sub("", res.stdout)


@dataclass
class Context:
    repo_root: Path
    importer: Callable[[str], Any]
    runner: Callable[..., str]


def make_ctx(repo_root: Path) -> Context:
    return Context(repo_root=repo_root, importer=_import, runner=_run)
