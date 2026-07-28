import subprocess
import sys
from pathlib import Path


def test_plugin_collects_docdrift_yml_as_test(tmp_path: Path):
    (tmp_path / ".docdrift.yml").write_text(
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - {extractor: files, path: cmds.txt, regex: '^(.+)$', format: '{item}'}\n"
    )
    (tmp_path / "cmds.txt").write_text("init\n")
    (tmp_path / "README.md").write_text("init\n")
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--rootdir", str(tmp_path), str(tmp_path)],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert "test_docdrift" in res.stdout
    assert res.returncode == 0, res.stdout + res.stderr


def test_plugin_fails_on_drift(tmp_path: Path):
    (tmp_path / ".docdrift.yml").write_text(
        "version: 1\ndocs: [README.md]\nsources:\n"
        "  - {extractor: files, path: cmds.txt, regex: '^(.+)$', format: '{item}'}\n"
    )
    (tmp_path / "cmds.txt").write_text("init\npush\n")
    (tmp_path / "README.md").write_text("init\n")  # push missing
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(tmp_path)],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert res.returncode != 0
    assert "push" in res.stdout
