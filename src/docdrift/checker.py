from __future__ import annotations

import docdrift.extractors  # noqa: F401  (register built-in extractors)
from docdrift.ctx import Context
from docdrift.manifest import Manifest
from docdrift.registry import ExtractorRegistry
from docdrift.reporting import DriftReport, SourceReport


def run(manifest: Manifest, ctx: Context) -> DriftReport:
    report = DriftReport()
    for src in manifest.sources:
        extractor = ExtractorRegistry.get(src.extractor)
        items = sorted(extractor.extract(src, ctx))
        literals = sorted(src.format.format(item=i) for i in items)
        doc_paths = src.docs or manifest.docs
        docs_text = "".join(
            (ctx.repo_root / p).read_text(encoding="utf-8", errors="replace")
            for p in doc_paths
        )
        missing = sorted(l for l in literals if l not in docs_text)
        report.add(SourceReport(
            name=src.name or src.extractor, extractor=src.extractor,
            items=items, literals=literals, missing=missing, docs=doc_paths,
        ))
    return report
