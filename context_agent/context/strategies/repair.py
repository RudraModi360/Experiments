"""Strategy 0: guarantee every assistant tool call has exactly one result."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional


class RepairStrategy:
    def __init__(self, emit: Callable[..., None]):
        self.emit = emit

    def apply(self, history: List[Dict[str, Any]], note: str = "") -> Optional[List[Dict[str, Any]]]:
        """Returns a replacement history when something was fixed, otherwise None."""
        fixed: List[Dict[str, Any]] = []
        changed = 0
        h, i = history, 0
        while i < len(h):
            m = h[i]
            if m["role"] == "tool":
                changed += 1
                i += 1
                continue
            if m["role"] == "assistant" and m.get("tool_calls"):
                n = len(m["tool_calls"])
                results, j = [], i + 1
                while j < len(h) and h[j]["role"] == "tool" and len(results) < n:
                    results.append(h[j])
                    j += 1
                fixed.append(m)
                fixed += results
                for k in range(len(results), n):
                    name = m["tool_calls"][k]["function"]["name"]
                    fixed.append({"role": "tool", "tool_name": name, "_meta": {"tool": name, "stubbed": True},
                                  "content": f"[no result: this call did not finish ({note or 'interrupted'})]"})
                    changed += 1
                i = j
                continue
            if m["role"] == "assistant" and not (m.get("content") or "").strip():
                changed += 1
                i += 1
                continue
            fixed.append(m)
            i += 1
        if changed:
            self.emit("repair", "fixed_history", changes=changed, note=note)
            return fixed
        return None
