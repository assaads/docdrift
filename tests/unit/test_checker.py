from pathlib import Path

from docdrift import checker
from docdrift.ctx import make_ctx
from docdrift.manifest import Manifest


def _manifest(format_: str = "syncestra {item}") -> Manifest:
    return Manifest.model_validate({
        "version": 1,
        "docs": ["README.md"],
        "sources": [
            {"extractor": "files", "path": "cmds.txt",
             "regex": r"^(.+)$", "format": format_},
        ],
    })


def test_checker_flags_missing_literals(tmp_path: Path):
    (tmp_path / "cmds.txt").write_text("init\npush\nstatus\n")  # 3 items
    (tmp_path / "README.md").write_text("syncestra init\nsyncestra push\n")  # status missing
    report = checker.run(_manifest(), make_ctx(tmp_path))
    assert report.has_drift() is True
    assert report.sources[0].missing == ["syncestra status"]


def test_checker_clean_when_all_present(tmp_path: Path):
    (tmp_path / "cmds.txt").write_text("init\npush\n")
    (tmp_path / "README.md").write_text("syncestra init\nsyncestra push\n")
    report = checker.run(_manifest(), make_ctx(tmp_path))
    assert report.has_drift() is False
    assert report.sources[0].missing == []


def test_render_summary_lists_missing(tmp_path: Path):
    (tmp_path / "cmds.txt").write_text("init\npush\nstatus\n")
    (tmp_path / "README.md").write_text("syncestra init\n")
    report = checker.run(_manifest(), make_ctx(tmp_path))
    text = report.render_summary()
    assert "syncestra push" in text and "syncestra status" in text


def test_checker_flags_missing_doc_file(tmp_path: Path):
    (tmp_path / "cmds.txt").write_text("init\npush\n")
    # NOTE: do NOT create README.md -> it is missing
    report = checker.run(_manifest(), make_ctx(tmp_path))
    assert report.has_drift() is True
    assert report.sources[0].missing_docs == ["README.md"]


def test_checker_no_boundary_splice_across_docs(tmp_path: Path):
    (tmp_path / "cmds.txt").write_text("init\n")
    (tmp_path / "A.md").write_text("syncestra ")      # ends mid-literal
    (tmp_path / "B.md").write_text("init")            # starts mid-literal
    m = Manifest.model_validate({
        "version": 1, "docs": ["A.md", "B.md"],
        "sources": [{"extractor": "files", "path": "cmds.txt", "regex": r"^(.+)$",
                     "format": "syncestra {item}"}],
    })
    report = checker.run(m, make_ctx(tmp_path))
    # the literal "syncestra init" is NOT wholly in either doc -> drift
    assert report.has_drift() is True
    assert report.sources[0].missing == ["syncestra init"]


def test_checker_warns_on_zero_items(tmp_path: Path):
    (tmp_path / "empty.txt").write_text("")  # regex matches nothing
    (tmp_path / "README.md").write_text("x")
    m = Manifest.model_validate({
        "version": 1, "docs": ["README.md"],
        "sources": [{"extractor": "files", "path": "empty.txt", "regex": r"^z$", "format": "{item}"}],
    })
    report = checker.run(m, make_ctx(tmp_path))
    assert "0 items" in report.render_summary()
