from pathlib import Path

import docdrift.extractors.python.click_ext  # noqa: F401
from docdrift.ctx import make_ctx
from docdrift.manifest import Source
from docdrift.registry import ExtractorRegistry


def test_click_extractor_lists_commands():
    src = Source(extractor="click", obj="app:cli")
    ctx = make_ctx(repo_root=Path(__file__).parent.parent / "fixtures" / "click_app")
    items = ExtractorRegistry.get("click").extract(src, ctx)
    assert {"build", "deploy"} <= items
