"""What the agent knows about each file, and whether that knowledge is still true."""

from __future__ import annotations

import os
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..utilities.files import file_version, merge_ranges, path_key
from ..utilities.text import clip


@dataclass
class FileRecord:
    path: str
    version: str = ""
    lines: Optional[int] = None
    reads: List[List[int]] = field(default_factory=list)  # ranges read at the CURRENT version
    created: bool = False
    writes: int = 0
    edits: int = 0
    last_ts: float = 0.0
    changed_externally: bool = False
    deleted: bool = False


class FileTracker:
    def __init__(self) -> None:
        self.records: Dict[str, FileRecord] = {}

    def reset(self) -> None:
        self.records.clear()

    def get(self, path: str) -> Optional[FileRecord]:
        return self.records.get(path_key(path))

    def note_read(self, path: str, start: int, end: int, total: Optional[int], version: str) -> bool:
        """Returns True when the file changed since we last saw it (outside our own writes)."""
        key = path_key(path)
        rec = self.records.get(key)
        changed = False
        if rec is None:
            rec = self.records[key] = FileRecord(path=os.path.abspath(path))
        elif rec.version and rec.version != version:
            changed = True
            rec.reads = []
        rec.version, rec.lines, rec.deleted = version, total, False
        if end >= start >= 1:
            rec.reads = merge_ranges(rec.reads + [[start, end]])
        rec.changed_externally = False
        rec.last_ts = time.time()
        return changed

    def note_write(self, path: str, version: str, lines: Optional[int], created: bool, edit: bool) -> None:
        key = path_key(path)
        rec = self.records.get(key)
        if rec is None:
            rec = self.records[key] = FileRecord(path=os.path.abspath(path))
        rec.version, rec.lines, rec.deleted = version, lines, False
        rec.reads = []  # we no longer hold a verified copy of the new content
        rec.changed_externally = False
        rec.created = rec.created or created
        if edit:
            rec.edits += 1
        else:
            rec.writes += 1
        rec.last_ts = time.time()

    def refresh(self) -> List[Tuple[str, str]]:
        """Detect changes made outside the agent. Returns [(key, new_version_or_'deleted')]."""
        changed = []
        for key, rec in self.records.items():
            current = file_version(rec.path)
            if current is None and not rec.deleted:
                rec.deleted, rec.reads, rec.changed_externally = True, [], True
                changed.append((key, "deleted"))
            elif current is not None and current != rec.version:
                rec.version, rec.reads, rec.changed_externally, rec.deleted = current, [], True, False
                changed.append((key, current))
        return changed

    def render(self, limit: int = 12) -> str:
        if not self.records:
            return ""
        recs = sorted(self.records.values(), key=lambda r: r.last_ts, reverse=True)[:limit]
        lines = ["FILES YOU HAVE TOUCHED (current state; copies in the conversation marked STALE are outdated):"]
        for rec in recs:
            bits = []
            if rec.created:
                bits.append("created by you")
            if rec.writes:
                bits.append(f"rewritten x{rec.writes}")
            if rec.edits:
                bits.append(f"edited x{rec.edits}")
            if rec.reads:
                bits.append("you hold lines " + ", ".join(f"{a}-{b}" for a, b in rec.reads))
            else:
                bits.append("no verified copy in context - re-read before relying on it")
            if rec.deleted:
                bits.append("DELETED on disk")
            elif rec.changed_externally:
                bits.append("CHANGED outside your edits")
            size = f"{rec.lines} lines" if rec.lines is not None else "size unknown"
            lines.append(clip(f"- {rec.path} | v{rec.version} | {size} | " + "; ".join(bits), 220))
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {k: asdict(v) for k, v in self.records.items()}

    def from_dict(self, data: Dict[str, Any]) -> None:
        self.records = {}
        for key, raw in (data or {}).items():
            try:
                self.records[key] = FileRecord(**raw)
            except TypeError:
                continue
