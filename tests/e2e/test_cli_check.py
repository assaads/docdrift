from pathlib import Path

from typer.testing import CliRunner

from docdrift.cli import app

runner = CliRunner()


def _repo(tmp_path: Path, *, docs_missing: bool = False) -> Path:
    (tmp_path / "cmds.txt").write_text("init\npush\n")
    (tmp_path / ".docdrift.yml").write_text(
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - {extractor: files, path: cmds.txt, regex: '^(.+)$', format: 'mycli {item}'}\n"
    )
    body = "mycli init\nmycli push\n" if not docs_missing else "mycli init\n"
    (tmp_path / "README.md").write_text(body)
    return tmp_path


def test_check_exit_0_when_in_sync(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(_repo(tmp_path))
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0, result.output


def test_check_exit_1_on_drift(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(_repo(tmp_path, docs_missing=True))
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 1, result.output
    assert "mycli push" in result.output


def test_list_prints_surface(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(_repo(tmp_path))
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0, result.output
    assert "init" in result.output and "push" in result.output
