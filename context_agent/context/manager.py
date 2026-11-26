"""ContextManager: composes the text-context strategies into the maintain() pipeline."""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from ..config import Config
from ..llm.errors import LLMError
from ..state.file_tracker import FileTracker
from ..state.working_state import WorkingState
from ..storage.session_store import SessionStore
from ..tools.result import ToolResult
from ..utilities.text import short_args
from .limits import BudgetPolicy, Limits
from .message import message_units, public_message
from .summarizer import ContextSummarizer
from .telemetry import ContextTelemetry, MaintainPass
from .token_counter import TokenCounter
from .trace import ContextTrace, ContextTraceEvent
from .view import ContextView
from .strategies.clear import OutputClearStrategy
from .strategies.compact import CompactionStrategy
from .strategies.dedupe import OutputDedupeStrategy
from .strategies.emergency import EmergencyStrategy
from .strategies.freshness import FreshnessStrategy
from .strategies.repair import RepairStrategy


class ContextManager:
    def __init__(self, cfg: Config, counter: TokenCounter, llm: Any, files: FileTracker,
                 state: WorkingState, store: SessionStore, tool_schemas: List[Dict[str, Any]]):
        self.cfg, self.counter, self.llm = cfg, counter, llm
        self.files, self.state, self.store = files, state, store
        self.history: List[Dict[str, Any]] = []
        self.force_compact = False
        self.actual_prompt_tokens: Optional[int] = None
        self.tools_tokens = int(counter.text(json.dumps(tool_schemas, ensure_ascii=False)) * 1.1)

        self.view = ContextView(counter, state, files, cfg=cfg)
        self.budget = BudgetPolicy(cfg, self.tools_tokens)
        self.trace_log = ContextTrace(cfg.verbose)
        self.trace: List[ContextTraceEvent] = self.trace_log.events
        self.telemetry = ContextTelemetry(cfg, getattr(store, "append_context_event", None))

        self.repair_strategy = RepairStrategy(self.note)
        self.freshness_strategy = FreshnessStrategy(self.note)
        self.dedupe_strategy = OutputDedupeStrategy()
        self.clear_strategy = OutputClearStrategy(
            self.note, self._save_full, on_clear_file=self.files.note_cleared, arg_limit=cfg.clear_arg_chars
        )
        self.summarizer = ContextSummarizer(cfg, llm, self.emit)
        self.compact_strategy = CompactionStrategy(counter, state, self.view, self.summarizer, self.note)
        self.emergency_strategy = EmergencyStrategy(self.clear_strategy, self.compact_strategy, self.view, self.note)

    # ------------------------------------------------------------------ plumbing
    def emit(self, stage: str, action: str, **details: Any) -> None:
        self.trace_log.verbose = self.cfg.verbose
        self.trace_log.emit(stage, action, **details)

    def note(self, stage: str, action: str, **details: Any) -> None:
        """Record a routine context event without printing it."""
        self.trace_log.append(stage, action, **details)

    @staticmethod
    def public(m: Dict[str, Any]) -> Dict[str, Any]:
        return public_message(m)

    def add(self, msg: Dict[str, Any]) -> None:
        self.history.append(msg)
        self.store.append_transcript({"ts": datetime.now().isoformat(timespec="seconds"), "msg": self.public(msg)})

    def reset(self) -> None:
        self.history = []
        self.force_compact = False

    def limits(self) -> Limits:
        return self.budget.limits()

    # ------------------------------------------------------------------ view
    def system_text(self) -> str:
        return self.view.system_text()

    def build_view(self, ephemeral: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.view.build(self.history, ephemeral)

    def view_tokens(self, ephemeral: Optional[str] = None) -> int:
        return self.view.tokens(self.history, ephemeral)

    def _count_tokens(self, history: List[Dict[str, Any]]) -> int:
        return self.view.tokens(history)

    # ------------------------------------------------------------------ structure
    def repair(self, note: str = "") -> None:
        fixed = self.repair_strategy.apply(self.history, note)
        if fixed is not None:
            self.history = fixed

    def units(self) -> List[Tuple[int, int]]:
        return message_units(self.history)

    # ------------------------------------------------------------------ freshness
    def mark_stale(self, key: str, version: str) -> int:
        return self.freshness_strategy.mark_stale(self.history, key, version)

    def refresh_files(self) -> None:
        self.freshness_strategy.refresh(self.files, self.history)

    # ------------------------------------------------------------------ ingestion
    def add_tool_result(self, name: str, args: Dict[str, Any], res: ToolResult) -> None:
        meta: Dict[str, Any] = {"tool": name, "args": short_args(args, 120), "ok": res.ok}
        meta.update(res.meta)
        sig = hashlib.sha1((name + json.dumps(args, sort_keys=True, default=str) + res.text)
                           .encode("utf-8", "replace")).hexdigest()[:12]
        meta["sig"] = sig
        if name != "edit_file" and meta.get("path") and meta.get("version"):
            self.mark_stale(meta["path"], meta["version"])
        self.dedupe_strategy.apply(self.history, name, meta)
        self.add({"role": "tool", "tool_name": name, "content": res.text, "_meta": meta})

    # ------------------------------------------------------------------ step 3: clear
    def _save_full(self, tag: str, text: str) -> str:
        digest = hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()[:10]
        os.makedirs(self.store.spill_dir, exist_ok=True)
        fname = f"{re.sub(r'[^A-Za-z0-9_]', '_', tag)}_{digest}.txt"
        path = os.path.join(self.store.spill_dir, fname)
        with open(path, "w", encoding="utf-8", errors="replace") as handle:
            handle.write(text)
        alias = f"spill/{fname}"
        self.state.add_saved(alias, f"{tag} output (cleared from context)")
        return alias

    def clear_old_outputs(self, target: int, keep_units: int, min_len: Optional[int] = None,
                          report: Optional[MaintainPass] = None) -> int:
        before = self.view_tokens()
        self.clear_strategy.arg_limit = self.cfg.clear_arg_chars
        effective_min = self.cfg.clear_min_chars if min_len is None else min_len
        cleared = self.clear_strategy.apply(self.history, target, keep_units, self._count_tokens, effective_min)
        if report is not None and cleared:
            report.masked(cleared, before, self.view_tokens())
        return cleared

    # ------------------------------------------------------------------ step 4: compact
    def compact(self, keep_tokens: int, use_llm: bool = True,
                report: Optional[MaintainPass] = None) -> bool:
        before, messages_before = self.view_tokens(), len(self.history)
        changed, history = self.compact_strategy.apply(self.history, keep_tokens, use_llm)
        self.history = history
        if report is not None and changed:
            report.compressed(folded=max(0, messages_before - len(history)), kept=len(history),
                              before=before, after=self.view_tokens(),
                              summary_chars=len(self.state.summary), llm=use_llm)
        return changed

    # ------------------------------------------------------------------ step 5: emergency
    def emergency(self, lim: Limits, report: Optional[MaintainPass] = None) -> None:
        before = self.view_tokens()
        self.history = self.emergency_strategy.apply(self.history, lim)
        if report is not None:
            report.emergency(before, self.view_tokens())

    # ------------------------------------------------------------------ orchestration
    def maintain(self) -> None:
        """Make room in the prompt, compressing (summary) before masking (stubs).

        Compression preserves knowledge in SESSION MEMORY; masking only removes
        raw tool output, which forces the agent to fetch it again.  The old
        order (clear first) meant compaction almost never ran, so long tasks
        turned into a clear/re-fetch loop.
        """
        self.repair()
        self.refresh_files()
        lim = self.limits()
        tokens = self.view_tokens()
        if tokens <= lim.trigger and not self.force_compact:
            return
        forced, self.force_compact = self.force_compact, False
        started = time.monotonic()
        item = MaintainPass(tokens_before=tokens, limit=lim.prompt_limit, trigger=lim.trigger,
                            clear_target=lim.clear_target, window=self.cfg.num_ctx,
                            reserve_out=self.cfg.num_predict, tools=self.tools_tokens,
                            forced=forced, actual_before=self.actual_prompt_tokens)
        self.note("budget", "over_trigger", tokens=tokens, trigger=lim.trigger,
                  limit=lim.prompt_limit, forced=forced)

        # 1. Compress: fold the oldest whole units into the rolling summary.
        if not self.compact(lim.keep, report=item):
            item.skipped("nothing_to_fold")
        tokens = self.view_tokens()

        # 2. Mask only as a fallback when compression could not reach the target.
        if tokens > lim.clear_target:
            if not self.clear_old_outputs(lim.clear_target, self.cfg.keep_recent_units, report=item):
                item.skipped("nothing_to_mask")
            tokens = self.view_tokens()

        # 3. Hard guarantee: never send a prompt above the usable window.
        if tokens > lim.prompt_limit:
            self.emergency(lim, report=item)
            tokens = self.view_tokens()

        item.tokens_after = tokens
        item.duration_ms = int((time.monotonic() - started) * 1000)
        self.telemetry.record(item)
