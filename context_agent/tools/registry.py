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

    @staticmethod
    def _smart_truncate(name: str, res: ToolResult, cap: int) -> str:
        """Preserve failure tracebacks in bash output; fall back to head_tail otherwise."""
        text = res.text
        if name == "bash" and (not res.ok or any(m in text for m in ("Traceback", "FAIL:", "ERROR:", "=== FAILURES ==="))):
            first_nl = text.find("\n")
            status = text[:first_nl] if first_nl != -1 else ""
            body = text[first_nl + 1:] if first_nl != -1 else text
            match = re.search(r"(?m)^(Traceback \(most recent call last\):|={3,}\s*FAILURES\s*={3,}|(?:FAIL|ERROR):\s+\S|E\s{3,}\S)", body)
            if match:
                tail_budget = int(cap * 0.25)
                fail_budget = max(400, cap - len(status) - tail_budget - 120)
                fail_slice = body[match.start(): match.start() + fail_budget]
                tail_slice = body[-tail_budget:] if len(body) > match.start() + fail_budget + tail_budget else ""
                parts = [p for p in (status, f"...[skipped {match.start()} header chars]..." if match.start() > 0 else "",
                                     fail_slice, "...[middle omitted]..." if tail_slice else "", tail_slice) if p]
                return "\n".join(parts)
        return head_tail(text, int(cap * 0.6), int(cap * 0.2))

    def _finalize(self, name: str, args: Dict[str, Any], res: ToolResult, cap: int) -> ToolResult:
        """Bound every result. Oversized output is saved in full and shown head + tail."""
        if res.capped or len(res.text) <= cap:
            return res
        path = self.context.save_spill(name, res.text)
        disp = self.context.short_path(path)
        self.state.add_saved(disp, f"{name}({short_args(args, 80)}) {len(res.text)} chars")
        lines = res.text.count("\n") + 1
        note = (f"[output truncated: {len(res.text)} chars / {lines} lines. Full copy: {disp} - "
                f"use read_file(path, offset, limit) or search_text(pattern, path)]")
        res.text = note + "\n" + self._smart_truncate(name, res, cap)
        res.meta["spill"] = path
        return res

    def _save_spill(self, tag: str, text: str) -> str:
        return self.context.save_spill(tag, text)
