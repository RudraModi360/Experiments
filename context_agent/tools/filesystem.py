"""File reading, writing and exact-text editing tools."""

from __future__ import annotations

import difflib
import os
import re
from typing import Any, Dict, List, Tuple

from ..utilities.file_text import decode_text_file, encode_text_file
from ..utilities.files import atomic_write_bytes, file_version, path_key
from ..utilities.formatting import fmt_size
from ..utilities.text import clip
from .constants import LINE_CAP, MAX_READ_BYTES
from .context import ToolExecutionContext
from .result import ToolError, ToolResult


class FileSystemTools:
    def __init__(self, ctx: ToolExecutionContext):
        self.ctx = ctx

    @property
    def files(self):
        return self.ctx.files

    def read_core(self, p: str, offset: int, limit: int, start_char: int, budget: int) -> Dict[str, Any]:
        if not os.path.exists(p):
            raise self.ctx.missing(p)
        if os.path.isdir(p):
            raise ToolError(f"'{p}' is a directory; use list_files")
        size = os.path.getsize(p)
        if size > MAX_READ_BYTES:
            raise ToolError(f"file is {fmt_size(size)}; too large to page. Use search_text.")
        with open(p, "rb") as handle:
            if b"\x00" in handle.read(8192):
                raise ToolError(f"'{p}' looks binary ({fmt_size(size)}); cannot read as text")
        version = file_version(p) or ""
        offset, limit, start_char = max(1, offset), max(1, min(limit, 2000)), max(0, start_char)
        out: List[str] = []
        used, total, last, full = 0, 0, 0, False
        with open(p, "rb") as handle:
            for index, raw in enumerate(handle, start=1):
                total = index
                if index < offset or full:
                    continue
                if len(out) >= limit:
                    full = True
                    continue
                line = raw.decode("utf-8", "replace").rstrip("\r\n")
                view = line[start_char:start_char + LINE_CAP]
                rest = len(line) - start_char - len(view)
                if rest > 0:
                    view += f" ...[+{rest} chars; start_char={start_char + LINE_CAP}]"
                entry = f"{index}| {view}"
                if out and used + len(entry) + 1 > budget:
                    full = True
                    continue
                out.append(entry)
                used += len(entry) + 1
                last = index
        return {"text": "\n".join(out), "first": offset if out else 0, "last": last,
                "total": total, "version": version}

    # Kept for compatibility with the original single-file Toolbox helper name.
    _read_core = read_core

    def read_file(self, path: str, offset: int = 1, limit: int = 200, start_char: int = 0) -> ToolResult:
        p = self.ctx.resolve(path)
        disp = self.ctx.short_path(p)
        info = self.read_core(p, offset, limit, start_char, max(800, self.ctx.cap - 400))
        first, last, total, version = info["first"], info["last"], info["total"], info["version"]
        spill = self.ctx.is_spill(p)
        header = f"[read_file {disp} | version {version} | "
        if not info["text"]:
            body = "(empty file)" if total == 0 else f"(offset {offset} is past the end; the file has {total} lines)"
            return ToolResult(header + f"{total} lines]\n" + body, capped=True)
        header += f"lines {first}-{last} of {total}"
        if last < total:
            header += f" | next: offset={last + 1}"
        header += "]"
        meta: Dict[str, Any] = {}
        if not spill:
            changed = self.files.note_read(p, first, last, total, version)
            meta = {"path": path_key(p), "display": disp, "version": version, "range": [first, last]}
            if changed:
                header += "\nNOTE: this file changed since you last saw it; older copies in the conversation are outdated."
        return ToolResult(header + "\n" + info["text"], meta=meta, capped=True)

    def write_file(self, path: str, content: str, overwrite: bool = False) -> ToolResult:
        p = self.ctx.resolve(path)
        disp = self.ctx.short_path(p)
        if os.path.isdir(p):
            raise ToolError(f"'{disp}' is a directory")
        existed = os.path.exists(p)
        newline, bom = "\n", False
        if existed:
            rec, current = self.files.get(p), file_version(p)
            if not overwrite:
                if rec is None:
                    raise ToolError(f"'{disp}' already exists and you have not read it in this session. "
                                    f"Read it first, or call write_file again with overwrite=true to replace it.")
                if rec.version != current:
                    raise ToolError(f"'{disp}' changed since you last saw it (v{rec.version} -> v{current}). "
                                    f"Read it again, or use overwrite=true.")
            try:
                _, newline, bom = decode_text_file(p)
            except ToolError:
                newline, bom = "\n", False
        text = content.replace("\r\n", "\n")
        atomic_write_bytes(p, encode_text_file(text, newline, bom))
        version = file_version(p) or ""
        lines = text.count("\n") + (0 if (text.endswith("\n") or not text) else 1)
        self.files.note_write(p, version, lines, created=not existed, edit=False)
        return ToolResult(f"{'Overwrote' if existed else 'Created'} {disp} ({lines} lines, {fmt_size(len(text.encode()))}, version {version}).",
                          meta={"path": path_key(p), "display": disp, "version": version}, capped=True)

    @staticmethod
    def _find_relaxed(lines: List[str], old_lines: List[str]) -> List[int]:
        """Start indexes where old_lines match, ignoring trailing whitespace."""
        target = [x.rstrip() for x in old_lines]
        n = len(target)
        return [i for i in range(len(lines) - n + 1) if [x.rstrip() for x in lines[i:i + n]] == target]

    def edit_file(self, path: str, old_content: str, new_content: str, replace_all: bool = False) -> ToolResult:
        p = self.ctx.resolve(path)
        disp = self.ctx.short_path(p)
        if not os.path.exists(p):
            raise self.ctx.missing(p)
        if os.path.isdir(p):
            raise ToolError(f"'{disp}' is a directory")
        text, newline, bom = decode_text_file(p)
        rec, before = self.files.get(p), file_version(p)
        warn = ""
        if rec is not None and rec.version != before:
            warn = f"NOTE: file changed since you last saw it (v{rec.version} -> v{before}).\n"
        old = old_content.replace("\r\n", "\n")
        new = new_content.replace("\r\n", "\n")
        if not old:
            raise ToolError("old_content is empty")
        if old == new:
            raise ToolError("old_content and new_content are identical; no change made.")

        spans: List[Tuple[int, int]] = []  # (start, end) character offsets in text
        idx = text.find(old)
        while idx != -1:
            spans.append((idx, idx + len(old)))
            idx = text.find(old, idx + max(1, len(old)))

        if not spans and re.match(r"^\s*\d+\|", old):  # model copied our line-number prefixes
            stripped = "\n".join(re.sub(r"^\s*\d+\|\s?", "", ln) for ln in old.split("\n"))
            if stripped and stripped in text:
                old = stripped
                new = "\n".join(re.sub(r"^\s*\d+\|\s?", "", ln) for ln in new.split("\n")) \
                    if re.match(r"^\s*\d+\|", new) else new
                idx = text.find(old)
                while idx != -1:
                    spans.append((idx, idx + len(old)))
                    idx = text.find(old, idx + max(1, len(old)))

        if not spans:  # whitespace-tolerant fallback
            lines = text.split("\n")
            starts = self._find_relaxed(lines, old.split("\n"))
            if starts:
                offsets = [0]
                for ln in lines:
                    offsets.append(offsets[-1] + len(ln) + 1)
                n = len(old.split("\n"))
                spans = [(offsets[i], offsets[i + n - 1] + len(lines[i + n - 1])) for i in starts]

        if not spans:
            first = old.split("\n")[0].strip()
            lines = [ln.strip() for ln in text.split("\n")]
            close = difflib.get_close_matches(first, lines, n=1, cutoff=0.6)
            hint = f" Closest line is {lines.index(close[0]) + 1}: {clip(close[0], 120)!r}." if close else ""
            raise ToolError("old_content was not found in the file." + hint +
                            " Re-read the relevant lines (read_file with offset/limit) and copy the exact text.")
        if len(spans) > 1 and not replace_all:
            where = ", ".join(str(text.count("\n", 0, s) + 1) for s, _ in spans[:8])
            raise ToolError(f"old_content matches {len(spans)} places (lines {where}). "
                            f"Add surrounding lines to make it unique, or set replace_all=true.")

        chosen = spans if replace_all else spans[:1]
        pieces, cursor = [], 0
        for start, end in chosen:
            pieces.append(text[cursor:start])
            pieces.append(new)
            cursor = end
        pieces.append(text[cursor:])
        updated = "".join(pieces)
        first_line = text.count("\n", 0, chosen[0][0]) + 1

        atomic_write_bytes(p, encode_text_file(updated, newline, bom))
        version = file_version(p) or ""
        new_lines = updated.split("\n")
        total = len(new_lines) - (1 if updated.endswith("\n") else 0)
        new_span_end = min(total, first_line + len(new.split("\n")) - 1)
        self.files.note_write(p, version, total, created=False, edit=True, read_range=[first_line, new_span_end])

        lo = max(1, first_line - 2)
        full_hi = min(total, first_line + len(new.split("\n")) + 1)
        hi = min(full_hi, lo + 23)
        snippet = "\n".join(f"{i}| {clip(new_lines[i - 1], 200)}" for i in range(lo, hi + 1))
        if full_hi > hi:
            snippet += f"\n... (+{full_hi - hi} more edited lines through line {full_hi})"
        return ToolResult(f"{warn}Edited {disp}: replaced {len(chosen)} occurrence(s), first at line {first_line}. "
                          f"New version {version}, {total} lines. Result around the change:\n{snippet}",
                          meta={"path": path_key(p), "display": disp, "version": version}, capped=True)
