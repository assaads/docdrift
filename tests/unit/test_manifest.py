from docdrift.manifest import Manifest, Source


def test_manifest_parses_typer_source_with_defaults():
    m = Manifest.model_validate({
        "version": 1,
        "docs": ["README.md"],
        "sources": [
            {"extractor": "typer", "module": "syncestra.cli", "app": "app",
             "format": "syncestra {item}"},
        ],
    })
    assert m.version == 1
    assert m.docs == ["README.md"]
    src = m.sources[0]
    assert src.extractor == "typer"
    assert src.format == "syncestra {item}"
    assert src.docs == []            # empty => inherit manifest.docs
    assert src.module == "syncestra.cli"   # extra="allow" keeps stack-specific fields
    assert src.app == "app"


def test_source_default_docs_and_format():
    src = Source(extractor="files")
    assert src.docs == []
    assert src.format == "{item}"
