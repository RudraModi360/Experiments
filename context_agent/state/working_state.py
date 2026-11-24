"""Durable working memory: summary, notes, plan, URLs and saved-output paths."""

from __future__ import annotations

from typing import Any, Dict, List

from ..config import Config
from ..utilities.text import clip
from .file_tracker import FileTracker


class WorkingState:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.reset()

    def reset(self) -> None:
        self.summary = ""
        self.plan = ""
        self.notes: Dict[str, str] = {}
        self.urls: Dict[str, str] = {}
        self.saved: List[Dict[str, str]] = []
        self.current_request = ""
        self.step = 0
        self.max_steps = 0

    def add_url(self, url: str, title: str = "") -> None:
        self.urls.pop(url, None)
        self.urls[url] = title
        while len(self.urls) > 30:
            self.urls.pop(next(iter(self.urls)))

    def add_saved(self, path: str, desc: str) -> None:
        self.saved = [s for s in self.saved if s["path"] != path]
        self.saved.append({"path": path, "desc": desc})
        self.saved = self.saved[-30:]

    def notes_chars(self) -> int:
        return sum(len(k) + len(v) for k, v in self.notes.items())

    def render_stable(self) -> str:
        parts = []
        if self.summary:
            parts.append("WHAT HAPPENED EARLIER (auto-compacted summary):\n" + self.summary)
        if self.notes:
            parts.append("YOUR SAVED NOTES:\n" + "\n".join(f"- {k}: {v}" for k, v in self.notes.items()))
        return "\n\n".join(parts)

    def render_volatile(self, files: FileTracker) -> str:
        sections = []
        if self.max_steps > 0:
            rem = max(0, self.max_steps - self.step)
            budget = f"BUDGET: step {self.step}/{self.max_steps}"
            if rem <= 3:
                budget += f" — WARNING: only {rem} step(s) left; finish remaining deliverables, verify, and summarize now."
            sections.append(budget)
        if self.plan:
            sections.append("PLAN (your checklist; keep it current with update_plan):\n" + clip(self.plan, 1200))
        file_block = files.render()
        if file_block:
            sections.append(file_block)
        if self.saved:
            rows = [clip(f"- {s['path']} <- {s['desc']}", 200) for s in self.saved[-6:]]
            sections.append("SAVED OUTPUTS (full copies; page with read_file or search_text):\n" + "\n".join(rows))
        if self.urls:
            rows = [clip(f"- {u} {t}".rstrip(), 160) for u, t in list(self.urls.items())[-8:]]
            sections.append("URLS SEEN:\n" + "\n".join(rows))
        return clip("\n\n".join(sections), self.cfg.max_ledger_chars)

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "plan": self.plan, "notes": self.notes, "urls": self.urls,
                "saved": self.saved, "current_request": self.current_request}

    def from_dict(self, data: Dict[str, Any]) -> None:
        self.reset()
        data = data or {}
        self.summary = data.get("summary", "")
        self.plan = data.get("plan", "")
        self.notes = dict(data.get("notes", {}))
        self.urls = dict(data.get("urls", {}))
        self.saved = list(data.get("saved", []))
        self.current_request = data.get("current_request", "")
