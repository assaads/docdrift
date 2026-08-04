from __future__ import annotations

import importlib
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def ensure_importable(dotted: str, repo_root: Path) -> None:
    """Ensure the import root for ``dotted``'s top-level package is on ``sys.path``.

    Consumer packages are not always importable from ``repo_root`` alone: a
    ``src/`` layout (``packages = ["src/<pkg>"]``) places the package at
    ``repo_root/src/<pkg>``, and under ``uvx`` the consumer's package is neither
    installed nor on the path. We derive the top-level name from ``dotted``
    (``syncestra.cli:app`` -> ``syncestra``) and search a small set of candidate
    roots for one that actually contains it — as a package dir
    (``<root>/<top>/__init__.py``) or a top-level module file
    (``<root>/<top>.py``) — prepending the first match. Purely a filesystem
    check: never imports, so it cannot pollute ``sys.modules`` (the caller pops
    the stale entry before importing).

    No-op if no candidate contains the package; the caller's import then either
    resolves via an existing ``sys.path`` entry (installed package) or raises.
    """
    top = dotted.replace(":", ".").split(".")[0]
    if not top:
        return
    # Candidate roots, most common first: repo_root, repo_root/src, repo_root/<pkg>.
    for root in (repo_root, repo_root / "src", repo_root / top):
        if (root / top / "__init__.py").is_file() or (root / f"{top}.py").is_file():
            _prepend(root)
            return


def _prepend(root: Path) -> None:
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


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
