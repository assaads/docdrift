from __future__ import annotations

import docdrift.extractors  # noqa: F401  (register built-in extractors)
from docdrift.config import DocdriftConfigError
from docdrift.ctx import Context
from docdrift.manifest import Manifest
from docdrift.registry import ExtractorRegistry
from docdrift.reporting import DriftReport, SourceReport


def run(manifest: Manifest, ctx: Context) -> DriftReport:
    report = DriftReport()
    for src in manifest.sources:
        extractor = ExtractorRegistry.get(src.extractor)
        items = sorted(extractor.extract(src, ctx))
        try:
            literals = sorted(src.format.format(item=i) for i in items)
        except (KeyError, IndexError, ValueError) as e:
            raise DocdriftConfigError(
                f"invalid format {src.format!r} for source {src.name or src.extractor!r}: {e}"
            ) from e
        doc_paths = src.docs or manifest.docs
        doc_texts: list[str] = []
        missing_docs: list[str] = []
        for p in doc_paths:
            fp = ctx.repo_root / p
            if fp.is_file():
                doc_texts.append(fp.read_text(encoding="utf-8", errors="replace"))
            else:
                missing_docs.append(p)
        missing = sorted(lit for lit in literals if not any(lit in t for t in doc_texts))
        report.add(SourceReport(
            name=src.name or src.extractor, extractor=src.extractor,
            items=items, literals=literals, missing=missing, docs=doc_paths,
            missing_docs=missing_docs,
        ))
    return report
