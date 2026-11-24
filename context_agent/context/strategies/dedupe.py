"""Strategy 2: identical and superseded tool outputs become stubs."""

from __future__ import annotations

from typing import Any, Dict, List

from ..message import stub_message


class OutputDedupeStrategy:
    def apply(self, history: List[Dict[str, Any]], name: str, meta: Dict[str, Any]) -> None:
        sig = meta.get("sig")
        for m in history:
            if m["role"] != "tool":
                continue
            old = m.get("_meta") or {}
            if old.get("stubbed") or old.get("cleared"):
                continue
            if old.get("sig") == sig:
                stub_message(m, "[duplicate: an identical output appears later in this conversation]")
            elif (name == "read_file" and old.get("tool") == "read_file" and old.get("path") == meta.get("path")
                  and old.get("version") == meta.get("version") and old.get("range") and meta.get("range")
                  and meta["range"][0] <= old["range"][0] and old["range"][1] <= meta["range"][1]):
                stub_message(m, f"[superseded by a later read of lines {meta['range'][0]}-{meta['range'][1]}]")
