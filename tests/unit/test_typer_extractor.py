import importlib
from pathlib import Path

import docdrift.extractors  # noqa: F401  (ensure registration import ran)
import docdrift.extractors.python.typer_ext  # noqa: F401
from docdrift.ctx import make_ctx
from docdrift.manifest import Source
from docdrift.registry import ExtractorRegistry


def test_typer_extractor_lists_commands():
    # fixture defines a typer app `app` with commands: init, push, status
    ExtractorRegistry._by_name.pop("typer", None)
    importlib.reload(docdrift.extractors.python.typer_ext)  # re-run @register

    src = Source(extractor="typer", module="app", app="app")  # module 'app' via fixture path
    ctx = make_ctx(repo_root=Path(__file__).parent.parent / "fixtures" / "typer_app")
    # importer needs the fixture on sys.path; the extractor adds repo_root via ctx
    items = ExtractorRegistry.get("typer").extract(src, ctx)
    assert {"init", "push", "status"} <= items
