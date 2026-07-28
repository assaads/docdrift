from pathlib import Path

import docdrift.extractors.python.argparse_ext  # noqa: F401
from docdrift.ctx import make_ctx
from docdrift.manifest import Source
from docdrift.registry import ExtractorRegistry


def test_argparse_extractor_lists_subcommands():
    src = Source(extractor="argparse", factory="app:build_parser")
    ctx = make_ctx(repo_root=Path(__file__).parent.parent / "fixtures" / "argparse_app")
    items = ExtractorRegistry.get("argparse").extract(src, ctx)
    assert {"fetch", "purge"} <= items
