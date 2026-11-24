"""Strategy 5: no-LLM fallback so a model call can never overflow the window."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from ...utilities.text import head_tail
from ..limits import Limits
from ..view import ContextView
from .clear import OutputClearStrategy
from .compact import CompactionStrategy


class EmergencyStrategy:
    def __init__(self, clear: OutputClearStrategy, compact: CompactionStrategy, view: ContextView,
                 emit: Callable[..., None]):
        self.clear = clear
        self.compact = compact
        self.view = view
        self.emit = emit

    def _truncate_largest(self, history: List[Dict[str, Any]], count_tokens: Callable[[List[Dict[str, Any]]], int],
                          limit: int) -> None:
        for _ in range(12):
            if count_tokens(history) <= limit or not history:
                return
            m = max(history, key=lambda item: self.view.counter.message(item))
            text = m.get("content") or ""
            if len(text) < 1200:
                return
            m["content"] = head_tail(text, max(400, len(text) // 4), max(200, len(text) // 8))
            self.emit("emergency", "truncated_message", role=m["role"], chars=len(text))

    def apply(self, history: List[Dict[str, Any]], lim: Limits) -> List[Dict[str, Any]]:
        def count_tokens(items: List[Dict[str, Any]]) -> int:
            return self.view.tokens(items)

        self.emit("emergency", "start", tokens=count_tokens(history), limit=lim.prompt_limit)
        self.clear.apply(history, 0, keep_units=1, count_tokens=count_tokens, min_len=200)
        for attempt in range(4):
            if count_tokens(history) <= lim.prompt_limit:
                return history
            changed, history = self.compact.apply(history, int(lim.keep * (0.6 ** attempt)), use_llm=False)
            if not changed:
                break
        self._truncate_largest(history, count_tokens, lim.prompt_limit)
        return history
