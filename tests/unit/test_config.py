from pathlib import Path

import pytest

from docdrift import config


def test_load_first_picks_first_existing(tmp_path: Path):
    f = tmp_path / ".docdrift.yml"
    f.write_text("version: 1\ndocs: [README.md]\nsources:\n"
                 "  - {extractor: files, path: 'src/**/*.py'}\n")
    m = config.load_first([tmp_path / "missing.yml", f])
    assert m.sources[0].extractor == "files"


def test_load_first_raises_if_none_found(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        config.load_first([tmp_path / "nope.yml"])


def test_rejects_wrong_version(tmp_path: Path):
    f = tmp_path / ".docdrift.yml"
    f.write_text("version: 2\nsources: []\n")
    with pytest.raises(config.DocdriftConfigError):
        config.load_first([f])


def test_rejects_non_dict_yaml(tmp_path: Path):
    f = tmp_path / ".docdrift.yml"
    f.write_text("- just\n- a\n- list\n")
    with pytest.raises(config.DocdriftConfigError):
        config.load_first([f])
