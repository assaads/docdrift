"""src-layout import support.

Consumer repos using a ``src/`` layout (``packages = ["src/<pkg>"]``) are NOT
importable from ``repo_root`` alone — the package lives at
``repo_root/src/<pkg>``. Under ``uvx`` (isolated env, package not installed)
the typer/click/argparse extractors must still find it. These tests fail
against the old ``sys.path.insert(0, repo_root)`` behavior and pass once the
extractors discover the package's import root.
"""
import importlib
from pathlib import Path

import docdrift.extractors  # noqa: F401  (ensure registration import ran)
import docdrift.extractors.python.typer_ext  # noqa: F401
from docdrift.ctx import make_ctx
from docdrift.manifest import Source
from docdrift.registry import ExtractorRegistry

_FIXTURE = Path(__file__).parent.parent / "fixtures" / "src_app"


def _reload_typer() -> None:
    ExtractorRegistry._by_name.pop("typer", None)
    importlib.reload(docdrift.extractors.python.typer_ext)  # re-run @register


def test_typer_extractor_finds_src_layout_package():
    """mycli.cli is at src/mycli/cli.py — not importable from repo_root alone."""
    _reload_typer()
    src = Source(extractor="typer", module="mycli.cli", app="app")
    ctx = make_ctx(repo_root=_FIXTURE)
    items = ExtractorRegistry.get("typer").extract(src, ctx)
    assert {"init", "deploy"} <= items
