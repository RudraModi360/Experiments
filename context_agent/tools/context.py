"""Shared execution context for tool implementations: paths, spilling and limits."""

from __future__ import annotations

import difflib
import hashlib
import os
import re
from typing import Iterator

from ..config import Config
from ..state.file_tracker import FileTracker
from ..state.working_state import WorkingState
from ..storage.session_store import SessionStore
from .constants import SKIP_DIRS
from .result import ToolError


class ToolExecutionContext:
    def __init__(self, cfg: Config, files: FileTracker, state: WorkingState, store: SessionStore):
        self.cfg = cfg
        self.files = files
        self.state = state
        self.store = store
        self.cap = cfg.max_tool_chars

    @property
    def spill_dir(self) -> str:
        return self.store.spill_dir

    @staticmethod
    def resolve(path: str) -> str:
        if not path or not path.strip():
            raise ToolError("empty path")
        return os.path.abspath(os.path.expanduser(path.strip()))

    def is_spill(self, path: str) -> bool:
        spill = os.path.normcase(os.path.abspath(self.store.spill_dir)) + os.sep
        return os.path.normcase(os.path.abspath(path)).startswith(spill)

    @staticmethod
    def display_path(path: str, base: str) -> str:
        try:
            return os.path.relpath(path, base)
        except ValueError:
            return path

    @staticmethod
    def walk_files(root: str, max_files: int = 5000) -> Iterator[str]:
        count = 0
        for cur, dirs, files in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(files):
                count += 1
                if count > max_files:
                    return
                yield os.path.join(cur, name)

    @staticmethod
    def missing(p: str) -> ToolError:
        hint = ""
        parent = os.path.dirname(p) or "."
        if os.path.isdir(parent):
            close = difflib.get_close_matches(os.path.basename(p), os.listdir(parent), n=3, cutoff=0.5)
            if close:
                hint = " Did you mean: " + ", ".join(close) + "?"
        return ToolError(f"'{p}' does not exist.{hint}")

    def save_spill(self, tag: str, text: str) -> str:
        digest = hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()[:10]
        os.makedirs(self.store.spill_dir, exist_ok=True)
        path = os.path.join(self.store.spill_dir, f"{re.sub(r'[^A-Za-z0-9_]', '_', tag)}_{digest}.txt")
        with open(path, "w", encoding="utf-8", errors="replace") as handle:
            handle.write(text)
        return path
