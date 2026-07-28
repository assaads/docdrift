import pytest

from docdrift.ctx import make_ctx
from docdrift.extractors.base import Extractor
from docdrift.registry import ExtractorRegistry, UnknownExtractor, register


def test_register_and_get():
    @register("demo")
    class Demo:
        name = "demo"

        def extract(self, source, ctx):  # type: ignore[no-untyped-def]
            return {"a", "b"}

    ext = ExtractorRegistry.get("demo")
    assert isinstance(ext, Extractor)
    assert ext.extract(None, None) == {"a", "b"}


def test_unknown_extractor_raises_with_list():
    with pytest.raises(UnknownExtractor) as ei:
        ExtractorRegistry.get("nope")
    assert "demo" in str(ei.value) or "available" in str(ei.value).lower()


def test_context_carries_repo_root():
    ctx = make_ctx(repo_root=__import__("pathlib").Path("/tmp"))
    assert ctx.repo_root.name == "tmp"
    assert callable(ctx.importer) and callable(ctx.runner)
