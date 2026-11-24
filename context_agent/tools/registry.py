"""Tool registry: schema validation, dispatch and output bounding."""

from __future__ import annotations

import json
import re
from typing import Any, Callable, Dict, List

from ..config import Config
from ..state.file_tracker import FileTracker
from ..state.working_state import WorkingState
from ..storage.session_store import SessionStore
from ..utilities.text import head_tail, short_args
from .context import ToolExecutionContext
from .bash import BashTool
from .filesystem import FileSystemTools
from .memory import MemoryTools
from .result import ToolError, ToolResult
from .search import SearchTools
from .specs import TOOL_SPECS
from .web import WebTools


class Toolbox:
    def __init__(self, cfg: Config, files: FileTracker, state: WorkingState, store: SessionStore):
        self.cfg = cfg
        self.files = files
        self.state = state
        self.store = store
        self.context = ToolExecutionContext(cfg, files, state, store)
        self.bash = BashTool(self.context)
        self.filesystem = FileSystemTools(self.context)
        self.search = SearchTools(self.context)
        self.web = WebTools(self.context, self.filesystem)
        self.memory = MemoryTools(cfg, state)
        self.schemas = TOOL_SPECS
        self._cap = cfg.max_tool_chars
        self._params = {s["function"]["name"]: s["function"]["parameters"] for s in TOOL_SPECS}
        self._handlers: Dict[str, Callable[..., ToolResult]] = {
            "bash": self.bash.run,
            "read_file": self.filesystem.read_file, "write_file": self.filesystem.write_file,
            "edit_file": self.filesystem.edit_file,
            "search_text": self.search.search_text, "search_files": self.search.search_files,
            "list_files": self.search.list_files,
            "web_search": self.web.web_search, "fetch_url": self.web.fetch_url,
            "update_plan": self.memory.update_plan, "save_note": self.memory.save_note,
        }

    # ------------------------------------------------------------------ dispatch
    def run(self, name: str, args: Any, cap: int) -> ToolResult:
        self._cap = self.context.cap = cap
        params = self._params.get(name)
        if params is None:
            return ToolResult(f"Unknown tool '{name}'. Available: {', '.join(self._handlers)}", ok=False)
        if not isinstance(args, dict):
            return ToolResult("Tool arguments must be a JSON object.", ok=False)
        if "__invalid_json__" in args:
            return ToolResult("Tool arguments were not valid JSON. Resend the call with a valid JSON object.", ok=False)
        try:
            props = params["properties"]
            clean, ignored = {}, []
            for key, value in args.items():
                if key not in props:
                    ignored.append(key)
                    continue
                clean[key] = self._coerce(props[key]["type"], value, key)
            missing = [r for r in params["required"] if r not in clean]
            if missing:
                return ToolResult(f"Missing required argument(s): {', '.join(missing)}. Expected: {', '.join(props)}", ok=False)
            res = self._handlers[name](**clean)
        except ToolError as exc:
            res = ToolResult(f"Error: {exc}", ok=False)
        except Exception as exc:  # a tool must never crash the agent loop
            res = ToolResult(f"Error in {name}: {type(exc).__name__}: {exc}", ok=False)
            clean, ignored = args, []
        if ignored:
            res.text += f"\n(ignored unknown argument(s): {', '.join(ignored)})"
        return self._finalize(name, clean, res, cap)

    @staticmethod
    def _coerce(kind: str, value: Any, key: str) -> Any:
        if kind == "integer":
            if isinstance(value, (bool, int, float)):
                return int(value)
            if isinstance(value, str) and re.fullmatch(r"-?\d+", value.strip()):
                return int(value)
            raise ToolError(f"argument '{key}' must be an integer")
        if kind == "boolean":
            if isinstance(value, bool):
                return value
            if isinstance(value, str) and value.strip().lower() in ("true", "1", "yes"):
                return True
            if isinstance(value, str) and value.strip().lower() in ("false", "0", "no"):
                return False
            raise ToolError(f"argument '{key}' must be true or false")
        if kind == "string":
            if isinstance(value, str):
                return value
            if isinstance(value, (dict, list)):
                return json.dumps(value, ensure_ascii=False, indent=2)
            return str(value)
        return value

    def _finalize(self, name: str, args: Dict[str, Any], res: ToolResult, cap: int) -> ToolResult:
        """Bound every result. Oversized output is saved in full and shown head + tail."""
        if res.capped or len(res.text) <= cap:
            return res
        path = self.context.save_spill(name, res.text)
        self.state.add_saved(path, f"{name}({short_args(args, 80)}) {len(res.text)} chars")
        head, tail = int(cap * 0.6), int(cap * 0.2)
        lines = res.text.count("\n") + 1
        note = (f"[output truncated: {len(res.text)} chars / {lines} lines. Full copy: {path} - "
                f"use read_file(path, offset, limit) or search_text(pattern, path)]")
        res.text = note + "\n" + head_tail(res.text, head, tail)
        res.meta["spill"] = path
        return res

    def _save_spill(self, tag: str, text: str) -> str:
        return self.context.save_spill(tag, text)
