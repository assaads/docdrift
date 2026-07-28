from __future__ import annotations

import glob
import re
from typing import Any

from docdrift.ctx import Context
from docdrift.registry import register


class _FilesLikeExtractor:
    """Glob files; optionally apply a regex (group 1 = item). Else item = file stem."""

    def extract(self, source: Any, ctx: Context) -> set[str]:
        pattern = getattr(source, "path", None) or getattr(source, "pattern", "")
        files = glob.glob(pattern, recursive=True, root_dir=str(ctx.repo_root))
        rx = getattr(source, "regex", None)
        compiled = re.compile(rx, re.MULTILINE) if rx else None
        items: set[str] = set()
        for rel in files:
            p = ctx.repo_root / rel
            if not p.is_file():
                continue
            if compiled is None:
                items.add(p.stem)
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            for m in compiled.finditer(text):
                if m.lastindex:  # a capture group exists
                    items.add(m.group(1))
        return items


@register("files")
class FilesExtractor(_FilesLikeExtractor):
    name = "files"


@register("regex")
class RegexExtractor(_FilesLikeExtractor):
    name = "regex"
