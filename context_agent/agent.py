"""Agent orchestration: turn loop, tool execution, persistence and slash commands."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .config import Config
from .context.manager import ContextManager
from .context.prompts import BASE_PROMPT
from .context.token_counter import TokenCounter
from .llm.errors import LLMError
from .llm.provider import create_llm
from .llm.reply import LLMReply
from .state.file_tracker import FileTracker
from .state.working_state import WorkingState
from .storage.session_store import SessionStore
from .tools.registry import Toolbox
from .utilities.formatting import color_enabled, dim, fail, fmt_tokens, ok, warn
from .utilities.text import clip, head_tail, short_args, strip_think


class IntelligentAgent:
    def __init__(self, cfg: Optional[Config] = None, llm: Any = None, resume: Optional[str] = None):
        self.cfg = cfg or Config()
        self.cfg.apply_context_scale()
        self.counter = TokenCounter()
        self.store = SessionStore(self.cfg)
        self.state = WorkingState(self.cfg)
        self.files = FileTracker()
        self.tools = Toolbox(self.cfg, self.files, self.state, self.store)
        self.llm = llm or create_llm(self.cfg)
        self.ctx = ContextManager(self.cfg, self.counter, self.llm, self.files, self.state, self.store,
                                  self.tools.schemas)
        self._loop_stop = False
        self._on_token: Optional[Callable[[str], None]] = None
        self._on_reply: Optional[Callable[[], None]] = None
        self._on_stats: Optional[Callable[[Dict[str, Any]], None]] = None
        self._last_chat_streamed = False
        self._streamed_content = False
        self.last_streamed = False
        self.last_stats: Optional[Dict[str, Any]] = None
        self.tool_stats: Dict[str, int] = {"calls": 0, "ok": 0, "failed": 0, "blocked": 0}
        if self.cfg.num_ctx < 8192:
            print(f"[warn] num_ctx={self.cfg.num_ctx} is small; tool definitions alone use ~{self.ctx.tools_tokens} tokens.")
        resumed = False
        if resume is not None:
            sid = resume or self.store.latest()
            resumed = bool(sid) and self.store.open_session(sid) and self._restore()
        if not resumed:
            self.store.new_session()
        self.store.prune(self.cfg.retention_days)

    # ------------------------------------------------------------------ persistence
    def _save(self) -> None:
        self.store.save_snapshot({
            "v": 2, "session": self.store.sid, "saved": datetime.now().isoformat(timespec="seconds"),
            "model": self.cfg.model, "provider": self.cfg.provider,
            "history": [self.ctx.public(m) for m in self.ctx.history],
            "state": self.state.to_dict(), "files": self.files.to_dict(), "scale": self.counter.scale})

    def _restore(self) -> bool:
        data = self.store.load_snapshot()
        if not data:
            return False
        self.ctx.history = data.get("history", [])
        self.state.from_dict(data.get("state", {}))
        self.files.from_dict(data.get("files", {}))
        self.counter.scale = float(data.get("scale", 1.0))
        self.ctx.repair("restored")
        self.ctx.refresh_files()  # anything that changed while we were away becomes STALE
        self.ctx.telemetry.load(self.store.read_context_events())
        return True

    # ------------------------------------------------------------------ commands
    def reset_session(self) -> str:
        self.ctx.reset()
        self.ctx.telemetry.reset()
        self.state.reset()
        self.files.reset()
        self._loop_stop = False
        self.store.new_session()
        self._save()
        return (f"Started a fresh session ({self.store.sid}). The previous conversation, summary, notes, plan, "
                f"file tracking and saved outputs are no longer in context (the old session stays on disk).")

    def resume_session(self, sid: str) -> str:
        """Open a saved session and restore its context."""
        if not self.store.open_session(sid):
            return f"No saved session '{sid}'."
        if not self._restore():
            return f"Session '{sid}' has no restorable state."
        self.ctx.force_compact = False
        self._loop_stop = False
        self.ctx.repair("resumed")
        self._save()
        return (f"Resumed session {self.store.sid} "
                f"({len(self.ctx.history)} messages in context, model {self.cfg.model}).")

    def switch_model(self, model: str) -> str:
        """Rebuild the LLM with a different model, keeping the conversation."""
        return self._swap_llm(model=model)

    def switch_provider(self, provider: str, model: Optional[str] = None) -> str:
        """Rebuild the LLM with a different provider, keeping the conversation."""
        return self._swap_llm(provider=provider, model=model)

    def set_context_window(self, num_ctx: Any) -> str:
        """Resize num_ctx and recompute all derived context/tool budgets live."""
        self.cfg.apply_context_scale(num_ctx)
        self.tools._cap = self.tools.context.cap = self.cfg.max_tool_chars
        self.ctx.clear_strategy.arg_limit = self.cfg.clear_arg_chars
        lim = self.ctx.limits()
        return (f"Context window set to {self.cfg.num_ctx} (num_predict={self.cfg.num_predict}, "
                f"usable_prompt={lim.prompt_limit}, max_tool_chars={self.cfg.max_tool_chars}, "
                f"keep_recent_units={self.cfg.keep_recent_units}).")

    def _swap_llm(self, provider: Optional[str] = None, model: Optional[str] = None) -> str:
        old = self.llm
        old_provider, old_model = self.cfg.provider, self.cfg.model
        if provider:
            self.cfg.provider = provider
        if model:
            self.cfg.model = model
        try:
            new = create_llm(self.cfg)
        except Exception:
            self.cfg.provider, self.cfg.model = old_provider, old_model
            raise
        self.llm = new
        self.ctx.llm = new
        self.ctx.summarizer.llm = new
        close = getattr(old, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass
        self._save()
        return f"Now using provider={self.cfg.provider} model={self.cfg.model}."

    def _command(self, text: str) -> Optional[str]:
        if not text.startswith("/"):
            return None
        cmd = text.split(None, 1)[0].lower()
        if cmd in ("/clear", "/new", "/reset"):
            return self.reset_session()
        if cmd == "/help":
            return ("/clear (/new, /reset)  fresh session\n/compact  force compaction now\n"
                    "/state  show memory + ledger\n/context  show token usage\n/quit  exit")
        if cmd == "/compact":
            lim, before = self.ctx.limits(), self.ctx.view_tokens()
            self.ctx.repair()
            self.ctx.clear_old_outputs(lim.clear_target, self.cfg.keep_recent_units)
            self.ctx.compact(lim.keep)
            self._save()
            return f"Context: {before} -> {self.ctx.view_tokens()} tokens (limit {lim.prompt_limit})."
        if cmd == "/state":
            return self.ctx.system_text().replace(BASE_PROMPT, "").strip() + "\n\n" + \
                (self.state.render_volatile(self.files) or "(no working state yet)")
        if cmd == "/context":
            lim, view = self.ctx.limits(), self.ctx.view_tokens()
            tools = self.ctx.tools_tokens
            actual = self.ctx.actual_prompt_tokens
            if not actual and self.ctx.telemetry.totals.get("last"):
                actual = self.ctx.telemetry.totals["last"].actual_before
            stubbed = sum(1 for m in self.ctx.history if (m.get("_meta") or {}).get("stubbed"))
            cleared = sum(1 for m in self.ctx.history if (m.get("_meta") or {}).get("cleared"))
            tool_msgs = sum(1 for m in self.ctx.history if m.get("role") == "tool")
            lines = [
                f"session {self.store.sid}",
                (f"window {fmt_tokens(self.cfg.num_ctx)} | out reserve {fmt_tokens(self.cfg.num_predict)} | "
                 f"tools {fmt_tokens(tools)} | usable prompt {fmt_tokens(lim.prompt_limit)} | "
                 f"trigger {fmt_tokens(lim.trigger)} | clear target {fmt_tokens(lim.clear_target)}"),
                (f"now view {fmt_tokens(view)} + tools {fmt_tokens(tools)} = {fmt_tokens(view + tools)} prompt"
                 + (f" | last actual {fmt_tokens(actual)}" if actual else "")
                 + f" | headroom {fmt_tokens(max(0, lim.prompt_limit - view))}"),
                (f"messages {len(self.ctx.history)} | tool results {tool_msgs} ({stubbed} stubbed, {cleared} cleared) | "
                 f"summary {len(self.state.summary)} chars | notes {len(self.state.notes)} | "
                 f"saved outputs {len(self.state.saved)}"),
                f"maintenance {self.ctx.telemetry.summary()}",
            ]
            recent = self.ctx.telemetry.recent(6)
            if recent:
                lines.append("recent passes (compress = folded into summary, mask = stubbed/cleared):")
                lines.extend("  " + item.render() for item in recent)
            lines.append(f"full event log: {os.path.join(self.store.dir, 'context_events.jsonl')}")
            return "\n".join(lines)
        return None  # unknown slash text (e.g. a path) goes to the model

    # ------------------------------------------------------------------ turn handling
    def process_query(self, user_input: str, on_token: Optional[Callable[[str], None]] = None,
                      on_reply: Optional[Callable[[], None]] = None,
                      on_stats: Optional[Callable[[Dict[str, Any]], None]] = None) -> str:
        self._on_token = on_token
        self._on_reply = on_reply
        self._on_stats = on_stats
        self.last_streamed = False
        self.last_stats = None
        user_input = (user_input or "").strip()
        if not user_input:
            return ""
        reply = self._command(user_input)
        if reply is not None:
            return reply
        self.tool_stats = {"calls": 0, "ok": 0, "failed": 0, "blocked": 0}
        try:
            self._start_turn(user_input)
            return self._run_turn()
        except KeyboardInterrupt:
            self.ctx.repair("interrupted by user")
            self._save()
            return "Interrupted. Context is intact - say 'continue' to resume or give a new instruction."
        except LLMError as exc:
            self.ctx.repair("model call failed")
            self._save()
            return f"Model error: {exc}\nYour request is kept in context; say 'continue' to retry."
        except Exception as exc:
            self.ctx.repair("internal error")
            self._save()
            return f"Internal error ({type(exc).__name__}): {exc}\nContext is intact; you can continue."

    _BOOKKEEPING_TOOLS = frozenset({"update_plan", "save_note"})
    _MAX_FREE_BOOKKEEPING = 6

    def _start_turn(self, text: str) -> None:
        self.ctx.repair()
        self.ctx.view.refresh_workspace()
        lim = self.ctx.limits()
        if self.counter.text(text) > int(lim.prompt_limit * self.cfg.max_user_ratio):
            path = self.tools._save_spill("user_message", text)
            disp = self.tools.context.short_path(path)
            self.state.add_saved(disp, f"user's long message ({len(text)} chars)")
            keep = int(lim.prompt_limit * self.cfg.max_user_ratio * 3.0)
            text = (f"[The user's message is very long ({len(text)} chars); the full text is saved at {disp}. "
                    f"Read it in pages with read_file or search it with search_text.]\n"
                    + head_tail(text, int(keep * 0.7), int(keep * 0.2)))
            self.ctx.emit("ingestion", "user_message_spilled", path=path)
        self.state.current_request = clip(text, 2500)
        self.ctx.add({"role": "user", "content": text})

    @staticmethod
    def _normalize_calls(calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for call in calls:
            fn = (call or {}).get("function") or {}
            args = fn.get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args) if args.strip() else {}
                except json.JSONDecodeError:
                    args = {"__invalid_json__": args[:300]}
            if not isinstance(args, dict):
                args = {}
            out.append({"function": {"name": fn.get("name") or "", "arguments": args}})
        return out

    def _record_stats(self, reply: LLMReply) -> None:
        """Accumulate token/timing stats across every model call in this turn."""
        stats = self.last_stats or {
            "prompt_tokens": 0, "output_tokens": 0, "duration": 0.0, "steps": 0,
            "tokens_per_second": None, "time_to_first_token": None,
            "prefill_tokens_per_second": None,
        }
        stats["prompt_tokens"] += reply.prompt_tokens or 0
        stats["output_tokens"] += reply.output_tokens or 0
        stats["duration"] += reply.duration or 0.0
        stats["steps"] += 1
        for key in ("tokens_per_second", "time_to_first_token", "prefill_tokens_per_second"):
            value = getattr(reply, key, None)
            if value is not None:
                stats[key] = value
        self.last_stats = stats
        if reply.prompt_tokens:
            self.ctx.actual_prompt_tokens = reply.prompt_tokens

    def _after_reply(self, estimated: int, reply: LLMReply) -> None:
        self.counter.calibrate(estimated + self.ctx.tools_tokens, reply.prompt_tokens)
        usable = self.ctx.limits().prompt_limit + self.ctx.tools_tokens
        if reply.prompt_tokens and reply.prompt_tokens >= int(usable * 0.97):
            self.ctx.force_compact = True
            self.ctx.emit("budget", "prompt_hit_window", prompt_tokens=reply.prompt_tokens,
                          usable=usable, num_ctx=self.cfg.num_ctx)

    def _chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]]) -> LLMReply:
        self._last_chat_streamed = False
        if self._on_reply:
            self._on_reply()
        try:
            if self._on_token is not None and getattr(self.llm, "supports_streaming", False):
                self._last_chat_streamed = True
                if self._on_stats is None:
                    return self.llm.chat_stream(messages, tools, on_token=self._on_token)
                return self.llm.chat_stream(messages, tools, on_token=self._on_token, on_stats=self._on_stats)
            return self.llm.chat(messages, tools)
        finally:
            # Close the live status before tool output / trace lines are printed,
            # so they never overwrite it and the next reply starts clean.
            if self._on_reply:
                self._on_reply()

    def _run_turn(self) -> str:
        steps, empties, ephemeral = 0, 0, None
        loop: Dict[str, List[Any]] = {}
        self._loop_stop = False
        while True:
            if steps >= self.cfg.max_steps_per_turn:
                return self._wrap_up("step limit reached")
            steps += 1
            self.state.step = steps
            self.state.max_steps = self.cfg.max_steps_per_turn
            self.ctx.maintain()
            view = self.ctx.build_view(ephemeral)
            ephemeral = None
            estimated = sum(self.counter.message(m) for m in view)
            reply = self._chat(view, self.tools.schemas)
            self._record_stats(reply)
            self._after_reply(estimated, reply)
            content = strip_think(reply.message.get("content") or "")
            calls = self._normalize_calls(reply.message.get("tool_calls") or [])
            if not calls:
                if not content:
                    empties += 1
                    if empties <= 2:
                        ephemeral = "Your last reply was empty. Continue with a tool call, or give your final answer."
                        continue
                    content = "(The model returned an empty response. Say 'continue' to retry.)"
                elif self._last_chat_streamed:
                    self.last_streamed = True
                self.ctx.add({"role": "assistant", "content": content})
                self._save()
                return content
            self.ctx.add({"role": "assistant", "content": content, "tool_calls": calls})
            self._streamed_content = bool(content) and self._last_chat_streamed
            self._execute_calls(calls, loop)
            self._save()
            if self._loop_stop:
                return self._wrap_up("the same call kept repeating without progress")

    # ------------------------------------------------------------------ tool output
    @staticmethod
    def _term_width() -> int:
        try:
            return shutil.get_terminal_size((80, 24)).columns or 80
        except Exception:
            return 80

    def _tool_header(self, status: str, name: str, args: Optional[Dict[str, Any]] = None,
                     note: str = "") -> str:
        icon = {"running": "⏳", "ok": "✓", "failed": "✗", "blocked": "⚠"}.get(status, "•")
        color = {"running": warn, "ok": ok, "failed": fail, "blocked": warn}.get(status, dim)
        bits = [color(f"{icon} [tool] {name}")]
        if args:
            prefix = f"{icon} [tool] {name} "
            budget = max(16, self._term_width() - len(prefix) - 3)  # icon is 2 cells
            bits.append(dim(short_args(args, budget)))
        if note:
            bits.append(color(note))
        return " ".join(bits)

    def _tool_start(self, name: str, args: Dict[str, Any]) -> bool:
        """Show an in-progress header; return True when it can be rewritten in place."""
        if not self.cfg.show_tools or not color_enabled():
            return False
        print(self._tool_header("running", name, args), flush=True)
        return True

    def _tool_done(self, name: str, status: str, note: str, text: str, rewrite: bool) -> None:
        if not self.cfg.show_tools:
            return
        line = self._tool_header(status, name, note=note)
        if rewrite:
            sys.stdout.write("\033[1A\r\033[2K" + line + "\n")
        else:
            print(line, flush=True)
        body = clip((text or "").strip(), 300)
        if not body:
            return
        paint = {"ok": dim, "failed": fail, "blocked": warn}.get(status, dim)
        for row in body.splitlines():
            print("    " + paint(row), flush=True)

    @staticmethod
    def _loop_key(name: str, args: Dict[str, Any]) -> str:
        if name == "bash" and isinstance(args.get("command"), str):
            cmd = re.sub(r"\s*2>(?:&1|/dev/null)\b", "", args["command"]).strip()
            cmd = re.sub(r"^pwd\s*&&\s*", "", cmd)
            cmd = re.sub(r"\s+", " ", cmd)
            if re.match(r"^(?:ls|pwd)\b", cmd):
                cmd = cmd.split()[0]
            elif re.match(r"^find\b", cmd):
                parts = cmd.split()
                target = parts[1] if len(parts) > 1 and not parts[1].startswith("-") else "."
                cmd = f"find:{os.path.normpath(target.strip(chr(39) + chr(34)))}"
            else:
                m = re.match(r"^(?:wc\s+-[lwc]+\s+\S+\s*&&\s*)?cat\s+(?:-[A-Za-z]+\s+)*(\S+)$", cmd)
                if m:
                    target = os.path.normpath(m.group(1).strip("'\""))
                    cmd = f"cat:{target}"
            return "bash:" + cmd + ":" + str(args.get("cwd", "."))
        return name + json.dumps(args, sort_keys=True, default=str)

    @staticmethod
    def _result_digest(name: str, text: str) -> str:
        norm = re.sub(r"\|\s*\d+\.\d+s\s*\|", "|", text) if name == "bash" else text
        return hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()

    def _execute_calls(self, calls: List[Dict[str, Any]], loop: Dict[str, List[Any]]) -> None:
        lim = self.ctx.limits()
        unit_chars = int(lim.prompt_limit * self.cfg.max_unit_ratio * 3.2)
        cap = max(800, min(self.cfg.max_tool_chars, unit_chars // max(1, len(calls))))
        if self.cfg.show_tools and self._streamed_content:
            print()
        for call in calls:
            name, args = call["function"]["name"], call["function"]["arguments"]
            rewrite = self._tool_start(name, args)
            res = self.tools.run(name, args, cap)
            key = self._loop_key(name, args)
            if name in ("write_file", "edit_file"):
                for k in [k for k in loop if k.startswith(("bash:ls:", "bash:pwd:", "bash:cat:", "bash:find:"))]:
                    loop.pop(k, None)
            digest = "inspect" if key.startswith(("bash:ls:", "bash:pwd:", "bash:cat:", "bash:find:")) else self._result_digest(name, res.text)
            count, last = loop.get(key, [0, None])
            count = count + 1 if last == digest else 1
            loop[key] = [count, digest]
            blocked = count >= self.cfg.loop_warn
            if blocked:
                res.ok = False
                res.text = (f"[loop-guard BLOCKED] You already ran {name} with identical results {count} times "
                            f"without modifying files. Output suppressed — edit the file, try a different command, "
                            f"or give your final answer.")
            if count >= self.cfg.loop_stop:
                self._loop_stop = True
            status = "blocked" if blocked else ("ok" if res.ok else "failed")
            if status == "blocked":
                note = f"BLOCKED · repeated {count}x"
            elif status == "ok":
                note = f"OK · {len(res.text)} chars"
            else:
                note = "FAILED"
            self.tool_stats["calls"] += 1
            self.tool_stats[status] += 1
            self._tool_done(name, status, note, res.text, rewrite)
            self.ctx.add_tool_result(name, args, res)

    def _mechanical_wrap_up(self, reason: str) -> str:
        parts = [f"Stopped early ({reason}). Current progress on disk:"]
        touched = sorted(self.files.records.values(), key=lambda r: r.last_ts, reverse=True)
        if touched:
            items = []
            for rec in touched[:10]:
                actions = []
                if rec.created:
                    actions.append("created")
                if rec.writes:
                    actions.append(f"written x{rec.writes}")
                if rec.edits:
                    actions.append(f"edited x{rec.edits}")
                tag = ", ".join(actions) if actions else "read"
                items.append(f"- {self.files._short_path(rec.path)} ({tag})")
            parts.append("Files:\n" + "\n".join(items))
        if self.state.plan:
            parts.append("Plan:\n" + clip(self.state.plan, 800))
        if self.state.notes:
            notes = "\n".join(f"- {k}: {clip(v, 200)}" for k, v in self.state.notes.items())
            parts.append("Notes:\n" + notes)
        parts.append("Progress is saved in context; say 'continue' to keep going.")
        return "\n\n".join(parts)

    def _wrap_up(self, reason: str) -> str:
        note = (f"Stop using tools now ({reason}). Reply briefly: what is done, what remains, "
                f"and the best next step.")
        text = ""
        try:
            self.ctx.maintain()
            reply = self._chat(self.ctx.build_view(note), None)
            text = strip_think(reply.message.get("content") or "")
        except LLMError:
            pass
        if text:
            suffix = f"\n\n(Stopped early: {reason}. Say 'continue' to resume.)"
            text += suffix
            if self._last_chat_streamed:
                self.last_streamed = True
                if self._on_token is not None:
                    self._on_token(suffix)
        else:
            text = self._mechanical_wrap_up(reason)
        self.ctx.add({"role": "assistant", "content": text})
        self._save()
        return text
