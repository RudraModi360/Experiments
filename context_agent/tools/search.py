"""Text search and directory listing tools."""

from __future__ import annotations

import os
import re
from typing import List

from ..utilities.formatting import fmt_size
from ..utilities.text import around
from .constants import MAX_SEARCH_FILE_BYTES, SKIP_DIRS
from .context import ToolExecutionContext
from .result import ToolError, ToolResult


class SearchTools:
    def __init__(self, ctx: ToolExecutionContext):
        self.ctx = ctx

    def search_text(self, pattern: str, path: str = ".", max_results: int = 30, context_lines: int = 0,
                    ignore_case: bool = True) -> ToolResult:
        note = ""
        flags = re.I if ignore_case else 0
        try:
            rx = re.compile(pattern, flags)
        except re.error:
            rx = re.compile(re.escape(pattern), flags)
            note = "(pattern was not a valid regex; searched literally)\n"
        root = self.ctx.resolve(path)
        if not os.path.exists(root):
            raise self.ctx.missing(root)
        base = root if os.path.isdir(root) else os.path.dirname(root)
        targets = list(self.ctx.walk_files(root)) if os.path.isdir(root) else [root]
        ctxn, limit = max(0, min(context_lines, 3)), max(1, min(max_results, 200))
        out: List[str] = []
        hits, scanned, more = 0, 0, False
        for target in targets:
            try:
                if os.path.getsize(target) > MAX_SEARCH_FILE_BYTES:
                    continue
                with open(target, "rb") as handle:
                    data = handle.read()
            except OSError:
                continue
            if b"\x00" in data[:8192]:
                continue
            lines = data.decode("utf-8", "replace").splitlines()
            scanned += 1
            rel = self.ctx.display_path(target, base) if os.path.isdir(root) else target
            for i, line in enumerate(lines):
                match = rx.search(line)
                if not match:
                    continue
                hits += 1
                if hits > limit:
                    more = True
                    break
                if ctxn:
                    lo, hi = max(0, i - ctxn), min(len(lines) - 1, i + ctxn)
                    block = [f"{rel}{':' if j == i else '-'}{j + 1}{':' if j == i else '-'} "
                             f"{around(lines[j], match.start() if j == i else 0)}" for j in range(lo, hi + 1)]
                    out.append("\n".join(block) + "\n--")
                else:
                    out.append(f"{rel}:{i + 1}: {around(line, match.start())}")
            if more:
                break
        shown = min(hits, limit)
        summary = f"{note}{shown} match(es) in {scanned} file(s) scanned" + (" - more exist, refine the pattern" if more else "")
        return ToolResult(summary + ("\n" + "\n".join(out) if out else ""))

    def search_files(self, pattern: str, directory: str = ".", max_results: int = 50) -> ToolResult:
        try:
            rx = re.compile(pattern, re.I)
        except re.error:
            rx = re.compile(re.escape(pattern), re.I)
        root = self.ctx.resolve(directory)
        if not os.path.isdir(root):
            raise ToolError(f"'{root}' is not a directory")
        limit, found, more = max(1, min(max_results, 500)), [], False
        for target in self.ctx.walk_files(root, max_files=50000):
            if rx.search(os.path.basename(target)):
                if len(found) >= limit:
                    more = True
                    break
                found.append(self.ctx.display_path(target, root))
        head = f"{len(found)} file(s) match '{pattern}' under {root}" + (" (more exist)" if more else "")
        return ToolResult(head + ("\n" + "\n".join(found) if found else ""))

    def list_files(self, directory: str = ".", max_depth: int = 2, max_entries: int = 150) -> ToolResult:
        root = self.ctx.resolve(directory)
        if not os.path.isdir(root):
            raise ToolError(f"'{root}' is not a directory")
        max_depth, max_entries = max(1, min(max_depth, 6)), max(1, min(max_entries, 500))
        base_depth = root.rstrip(os.sep).count(os.sep)
        lines: List[str] = []
        truncated = False
        for cur, dirs, files in os.walk(root):
            depth = cur.rstrip(os.sep).count(os.sep) - base_depth
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            entries = [(d, None) for d in dirs] + [(f, f) for f in sorted(files)]
            for name, is_file in entries:
                if len(lines) >= max_entries:
                    truncated = True
                    break
                full = os.path.join(cur, name)
                rel = self.ctx.display_path(full, root)
                if is_file:
                    try:
                        lines.append(f"{rel} ({fmt_size(os.path.getsize(full))})")
                    except OSError:
                        lines.append(rel)
                else:
                    lines.append(rel + os.sep)
            if truncated:
                break
            if depth + 1 >= max_depth:
                dirs[:] = []
        head = f"{len(lines)} entries under {root} (depth {max_depth})" + (" - truncated; narrow the directory" if truncated else "")
        return ToolResult(head + ("\n" + "\n".join(lines) if lines else ""))
