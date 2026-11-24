"""Strategy 3: shrink old large tool outputs and call arguments to stubs."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from ..message import message_units


class OutputClearStrategy:
    def __init__(self, emit: Callable[..., None], save_full: Callable[[str, str], str]):
        self.emit = emit
        self.save_full = save_full

    @staticmethod
    def _shrink_args(m: Dict[str, Any]) -> bool:
        meta = m.setdefault("_meta", {})
        if meta.get("args_shrunk"):
            return False
        changed = False
        for call in m.get("tool_calls") or []:
            args = call["function"].get("arguments")
            if isinstance(args, dict):
                for key, value in list(args.items()):
                    if isinstance(value, str) and len(value) > 600:
                        args[key] = value[:200] + f"...[{len(value) - 200} more chars omitted from history]"
                        changed = True
        meta["args_shrunk"] = True
        return changed

    def _clear_tool_message(self, m: Dict[str, Any]) -> bool:
        meta = m.setdefault("_meta", {})
        if meta.get("cleared") or meta.get("stubbed"):
            return False
        text = m.get("content") or ""
        tool = meta.get("tool") or m.get("tool_name") or "tool"
        if tool == "read_file" and meta.get("path"):
            rng = meta.get("range") or ["?", "?"]
            stub = (f"[CLEARED to save context: read_file {meta.get('display', meta['path'])} lines {rng[0]}-{rng[1]} "
                    f"(v{meta.get('version')}) - re-read it if you need the content]")
        else:
            path = meta.get("spill") or self.save_full(tool, text)
            start = " ".join(text[:200].split())
            stub = (f"[CLEARED to save context: {tool}({meta.get('args', '')}) -> {len(text)} chars. "
                    f"Starts: {start!r}. Full copy: {path}]")
        meta["full"], meta["cleared"] = text, True
        m["content"] = stub
        return True

    def apply(self, history: List[Dict[str, Any]], target: int, keep_units: int,
              count_tokens: Callable[[List[Dict[str, Any]]], int], min_len: int = 500) -> int:
        units = message_units(history)
        n = 0
        for start, end in units[: max(0, len(units) - keep_units)]:
            for k in range(start, end):
                m = history[k]
                if m["role"] == "assistant":
                    n += int(self._shrink_args(m))
                elif m["role"] == "tool" and len(m.get("content") or "") > min_len:
                    n += int(self._clear_tool_message(m))
            if target and count_tokens(history) <= target:
                break
        return n
