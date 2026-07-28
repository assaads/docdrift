import re  # noqa: F401
from pathlib import Path

from docdrift.ctx import make_ctx
from docdrift.manifest import Source
from docdrift.registry import ExtractorRegistry

import docdrift.extractors.generic.files_ext  # noqa: F401

REPO = Path(__file__).parent.parent / "fixtures" / "files_repo"


def test_files_extractor_returns_stems():
    src = Source(extractor="files", path="src/**/*.py")
    items = ExtractorRegistry.get("files").extract(src, make_ctx(REPO))
    assert {"alpha", "beta"} <= items


def test_files_extractor_with_regex_capture():
    # src/cli.py has `def init`, `def push` -> capture def names
    src = Source(extractor="regex", path="src/cli.py",
                 regex=r"^def (\w+)\b")
    items = ExtractorRegistry.get("regex").extract(src, make_ctx(REPO))
    assert {"init", "push"} <= items
