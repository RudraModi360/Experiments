"""Strategy 1: file changes make older read outputs STALE."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from ...state.file_tracker import FileTracker
from ..message import stub_message


class FreshnessStrategy:
    def __init__(self, emit: Callable[..., None]):
        self.emit = emit

    @staticmethod
    def mark_stale(history: List[Dict[str, Any]], key: str, version: str) -> int:
        n = 0
        for m in history:
            meta = m.get("_meta") or {}
            if m["role"] == "tool" and meta.get("path") == key and meta.get("version") \
                    and meta["version"] != version and not meta.get("stubbed"):
                rng = meta.get("range")
                what = f"{meta.get('tool')} of {meta.get('display', key)}" + (f" lines {rng[0]}-{rng[1]}" if rng else "")
                stub_message(m, f"[STALE: {what} (v{meta['version']}) - the file has since changed (now v{version}). "
                                f"Re-read it before relying on this.]")
                n += 1
        return n

    def refresh(self, files: FileTracker, history: List[Dict[str, Any]]) -> None:
        changed = files.refresh()
        for key, version in changed:
            self.mark_stale(history, key, version)
        if changed:
            self.emit("freshness", "files_changed_outside_agent", files=[k for k, _ in changed])
