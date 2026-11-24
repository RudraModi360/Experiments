"""Tools that write durable working memory (plan and notes)."""

from __future__ import annotations

from ..config import Config
from ..state.working_state import WorkingState
from ..utilities.text import clip
from .result import ToolError, ToolResult


class MemoryTools:
    def __init__(self, cfg: Config, state: WorkingState):
        self.cfg = cfg
        self.state = state

    def update_plan(self, plan: str) -> ToolResult:
        self.state.plan = plan.strip()[:1500]
        return ToolResult("Plan updated.", capped=True)

    def save_note(self, key: str, content: str) -> ToolResult:
        key, content = clip(key.strip(), 40), content.strip()
        if not key:
            raise ToolError("note key is empty")
        if not content:
            self.state.notes.pop(key, None)
            return ToolResult(f"Deleted note '{key}'.", capped=True)
        content = clip(content, 500)
        old = self.state.notes.pop(key, "")
        if self.state.notes_chars() + len(key) + len(content) > self.cfg.max_notes_chars:
            if old:
                self.state.notes[key] = old
            raise ToolError("notes are full; delete or shorten older notes first (save_note(key, '') deletes)")
        self.state.notes[key] = content
        return ToolResult(f"Saved note '{key}'.", capped=True)
