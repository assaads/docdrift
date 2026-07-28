"""pytest11 entry point: a .docdrift.yml at repo root becomes one test_docdrift.

A `.docdrift.yml` dropped at a repo root is collected as a single pytest item
named ``test_docdrift``; the item fails (raising ``AssertionError`` with the
drift summary) whenever docs drift from sources.

Note on the ``DocdriftItem`` path handling: under pytest 8/9 ``Item.from_parent``
does not reliably honour a ``path=`` kwarg, and ``pytest.Item`` does not store a
``.path`` attribute the way ``pytest.File`` does. We therefore capture the
manifest path from the parent ``File`` explicitly (``docdrift_path``) and use it
in ``runtest``/``reportinfo``.

A small ``pytest_report_collectionfinish`` hook reports the collected docdrift
item. pytest prints this hook's output even under ``-q`` (where passing tests
are otherwise shown only as a dot), which makes the docdrift test discoverable
in quiet CI logs.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from docdrift import checker as checker_mod
from docdrift import config as config_mod
from docdrift import ctx as ctx_mod


def pytest_collect_file(parent, file_path):  # type: ignore[no-untyped-def]
    if file_path.name == ".docdrift.yml":
        return DocdriftFile.from_parent(parent, path=file_path)


def pytest_report_collectionfinish(config, start_path, items):  # type: ignore[no-untyped-def]
    """Announce collected docdrift tests (visible even under ``-q``)."""
    collected = [i.name for i in items if isinstance(i, DocdriftItem)]
    if collected:
        return [f"docdrift: {', '.join(collected)}"]
    return []


class DocdriftFile(pytest.File):
    def collect(self):  # type: ignore[no-untyped-def]
        yield DocdriftItem.from_parent(self, name="test_docdrift")


class DocdriftItem(pytest.Item):
    def __init__(self, *, name, parent):  # type: ignore[no-untyped-def]
        super().__init__(name=name, parent=parent)
        # pytest 8/9 Item does not reliably expose ``.path``; capture from parent.
        self.docdrift_path = parent.path

    def runtest(self):  # type: ignore[no-untyped-def]
        manifest = config_mod.load_first([Path(self.docdrift_path)])
        rootpath = (
            Path(str(self.config.rootpath)) if self.config.rootpath
            else Path(self.docdrift_path).parent
        )
        report = checker_mod.run(manifest, ctx_mod.make_ctx(rootpath))
        if report.has_drift():
            raise AssertionError(report.render_summary())

    def reportinfo(self):  # type: ignore[no-untyped-def]
        return (self.docdrift_path, 0, "docs-drift")
