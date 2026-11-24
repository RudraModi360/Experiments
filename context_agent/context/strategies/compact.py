"""Strategy 4: fold the oldest whole units into a rolling summary."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple

from ...state.working_state import WorkingState
from ..message import message_units
from ..summarizer import ContextSummarizer
from ..token_counter import TokenCounter
from ..view import ContextView


class CompactionStrategy:
    def __init__(self, counter: TokenCounter, state: WorkingState, view: ContextView,
                 summarizer: ContextSummarizer, emit: Callable[..., None]):
        self.counter = counter
        self.state = state
        self.view = view
        self.summarizer = summarizer
        self.emit = emit

    def apply(self, history: List[Dict[str, Any]], keep_tokens: int,
              use_llm: bool = True) -> Tuple[bool, List[Dict[str, Any]]]:
        units = message_units(history)
        if len(units) <= 1:
            self.emit("compression", "skipped", reason="only_one_unit")
            return False, history
        fixed = self.counter.text(self.view.system_text()) + 700  # system + working-state tail
        budget = max(400, keep_tokens - fixed)
        acc, start_unit = 0, len(units)
        for ui in range(len(units) - 1, -1, -1):
            s, e = units[ui]
            cost = sum(self.counter.message(history[k]) for k in range(s, e))
            if start_unit < len(units) and acc + cost > budget:
                break
            acc += cost
            start_unit = ui
        if start_unit == 0:
            self.emit("compression", "skipped", reason="everything_fits_in_keep_window")
            return False, history
        cut = units[start_unit][0]
        old = history[:cut]
        before = self.view.tokens(history)
        self.state.summary = self.summarizer.fold(old, self.state.summary, use_llm)
        new_history = history[cut:]
        self.emit("compression", "compacted", folded_messages=len(old), kept_messages=len(new_history),
                  tokens_before=before, tokens_after=self.view.tokens(new_history), llm=use_llm)
        return True, new_history
