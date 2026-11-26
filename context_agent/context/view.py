"""Builds the exact message list the model sees."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from ..state.file_tracker import FileTracker
from ..state.working_state import WorkingState
from ..tools.constants import SKIP_DIRS
from .message import clean_message
from .prompts import BASE_PROMPT
from .token_counter import TokenCounter


class ContextView:
    def __init__(self, counter: TokenCounter, state: WorkingState, files: FileTracker,
                 base_prompt: str = BASE_PROMPT, cfg: Any = None):
        self.counter = counter
        self.state = state
        self.files = files
        self.base_prompt = base_prompt
        self.cfg = cfg
        self._workspace_snapshot_cache: Optional[str] = None

    @staticmethod
    def _workspace_snapshot(max_depth: int = 2, max_entries: int = 40) -> str:
        try:
            root = os.getcwd()
            base_depth = root.rstrip(os.sep).count(os.sep)
            entries: List[str] = []
            top_dirs: List[str] = []
            extra = 0
            for cur, dirs, files in os.walk(root):
                depth = cur.rstrip(os.sep).count(os.sep) - base_depth
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                if depth == 0:
                    top_dirs = [d + "/" for d in dirs]
                for fname in sorted(files):
                    if fname == ".DS_Store":
                        continue
                    rel = os.path.relpath(os.path.join(cur, fname), root)
                    if len(entries) < max_entries:
                        entries.append(rel)
                    else:
                        extra += 1
                if depth + 1 >= max_depth:
                    for dname in dirs:
                        rel = os.path.relpath(os.path.join(cur, dname), root) + "/"
                        if len(entries) < max_entries:
                            entries.append(rel)
                        else:
                            extra += 1
                    dirs[:] = []
            if entries:
                listing = ", ".join(entries)
                suffix = f" (+{extra} more)" if extra else ""
                return f"Existing workspace files (read before overwriting): {listing}{suffix}"
            if top_dirs:
                shown = ", ".join(top_dirs[:max_entries])
                return f"Workspace status: empty (0 files; empty directories: {shown})"
            return "Workspace status: empty (0 files)"
        except OSError:
            return ""

    def refresh_workspace(self) -> None:
        max_entries = getattr(self.cfg, "workspace_snapshot_entries", None) or 40
        self._workspace_snapshot_cache = self._workspace_snapshot(max_entries=max_entries)

    def system_text(self) -> str:
        if self._workspace_snapshot_cache is None:
            self.refresh_workspace()
        base = self.base_prompt
        if self._workspace_snapshot_cache:
            base += f"\n\n{self._workspace_snapshot_cache}"
        stable = self.state.render_stable()
        if not stable:
            return base
        return (base + "\n\n=== SESSION MEMORY (background from earlier in this session; the user's newest "
                "message always takes priority) ===\n" + stable + "\n=== END SESSION MEMORY ===")

    def build(self, history: List[Dict[str, Any]], ephemeral: Optional[str] = None) -> List[Dict[str, Any]]:
        view = [{"role": "system", "content": self.system_text()}]
        body = [clean_message(m) for m in history]
        if body and body[0]["role"] != "user":  # many chat templates require a user turn first
            request = self.state.current_request or "(see SESSION MEMORY)"
            body.insert(0, {"role": "user", "content":
                            "[Earlier messages were compacted into SESSION MEMORY.] Current request from the user:\n" + request})
        view += body
        parts = []
        tail = self.state.render_volatile(self.files)
        if tail:
            parts.append("[WORKING STATE - automatic bookkeeping, not written by the user. "
                         "Their request is the last real user message above.]\n" + tail)
        if ephemeral:
            parts.append(ephemeral)
        if parts:
            view.append({"role": "user", "content": "\n\n".join(parts)})
        return view

    def tokens(self, history: List[Dict[str, Any]], ephemeral: Optional[str] = None) -> int:
        return sum(self.counter.message(m) for m in self.build(history, ephemeral))
