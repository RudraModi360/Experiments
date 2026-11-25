"""Live per-case progress for eval runs.

``deepeval test run`` executes the suite through pytest, which captures stdout.
A plain ``print`` therefore only appears after a case finishes (or when it
fails), so while the agent is working there is no way to see *which* case of the
suite is currently running.

This module writes a one-row ``[eval]`` status straight to the terminal - the
same idea as the CLI's live ``[stats]`` telemetry line - so the current case,
its position in the suite, the phase (workspace / agent / checks / judging),
elapsed time, steps and tool calls stay visible while the run is in progress.

When there is no interactive terminal (CI, redirected output) it falls back to
static ``[eval]`` start/finish lines, which are also captured by pytest and
shown with the failure output.
"""

from __future__ import annotations

import os
import shutil
import sys
import threading
import time
from typing import Any, Optional, TextIO

_CLEAR_LINE = "\r\033[2K"
_TERMINAL: Optional[TextIO] = None
_TERMINAL_READY = False


def _print_is_tty() -> bool:
    """Whether a plain ``print`` already reaches the terminal (no capture)."""
    return bool(getattr(sys.stdout, "isatty", lambda: False)())


def _live_enabled() -> bool:
    flag = os.environ.get("EVAL_LIVE_PROGRESS", "").strip().lower()
    if flag in {"0", "false", "no", "off"}:
        return False
    # Multiple xdist workers would fight over the same terminal row.
    if os.environ.get("PYTEST_XDIST_WORKER"):
        return False
    return True


def _terminal_stream() -> Optional[TextIO]:
    """Return a writable terminal handle that bypasses pytest's capture.

    pytest's default fd capture also redirects ``sys.__stdout__``, so
    ``isatty`` on the Python stream cannot be trusted.  Opening ``/dev/tty``
    succeeds only when the process actually owns a controlling terminal, which
    is exactly the case where a live line makes sense.
    """
    global _TERMINAL, _TERMINAL_READY
    if _TERMINAL_READY:
        return _TERMINAL
    _TERMINAL_READY = True
    if not _live_enabled():
        return None
    try:
        # /dev/tty is not redirected by pytest's fd capture. It also works when
        # stdout is piped while the process still owns a terminal.
        _TERMINAL = open("/dev/tty", "w", encoding="utf-8", buffering=1)
    except OSError:  # Windows / no controlling terminal
        stream = getattr(sys, "__stdout__", None)
        _TERMINAL = stream if stream is not None and getattr(stream, "isatty", lambda: False)() else None
    return _TERMINAL


def _paint(text: str, code: str) -> str:
    if os.environ.get("NO_COLOR") is not None:
        return text
    return f"\033[{code}m{text}\033[0m"


def _clock(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _fit(text: str, width: int) -> str:
    if width <= 1 or len(text) <= width:
        return text
    return text[: width - 1] + "…"


class CaseProgress:
    """One pinned ``[eval]`` status line for the case currently under test."""

    def __init__(
        self,
        case: Any,
        index: int,
        total: int,
        *,
        suite: str = "single",
        stream: Optional[TextIO] = None,
        interval: float = 0.5,
    ) -> None:
        self.case = case
        self.index = int(index)
        self.total = int(total)
        self.suite = suite
        self.phase = "workspace"
        self.steps = 0
        self.tools = 0
        self.tool_errors = 0
        self.last_tool = ""
        self.started = time.monotonic()
        self._stream = stream if stream is not None else _terminal_stream()
        self._live = self._stream is not None
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._drawn = False
        self._finished = False
        self._interval = max(0.0, float(interval))
        self._width = max(40, shutil.get_terminal_size(fallback=(100, 24)).columns)

    # -- lifecycle ---------------------------------------------------------

    def __enter__(self) -> "CaseProgress":
        self._emit_line(
            f"[eval] {self._head()} "
            f"| profile={self.case.profile or 'case'} | starting"
        )
        self._start_ticker()
        self._draw()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if not self._finished:
            error = None
            if exc_type is not None:
                error = f"{exc_type.__name__}: {exc}"
            self.finish(error=error)
        return False

    def _start_ticker(self) -> None:
        if not self._live or self._interval <= 0 or self._thread is not None:
            return
        self._thread = threading.Thread(
            target=self._tick, name="eval-progress", daemon=True
        )
        self._thread.start()

    def _tick(self) -> None:
        while not self._stop.wait(self._interval):
            # DeepEval draws its own indicator while the judge runs; stay quiet
            # then so the two status areas never fight over the same row.
            if self.phase != "judging":
                self._draw()

    def _elapsed(self) -> float:
        return time.monotonic() - self.started

    # -- updates -----------------------------------------------------------

    def set_phase(self, phase: str) -> None:
        """Mark the current stage (workspace / agent / checks / judging / report)."""
        self.phase = phase
        if phase == "judging":
            self._clear()
            self._emit_line(
                f"[eval] {self._head()} "
                f"| judging metrics | {_clock(self._elapsed())}"
            )
        else:
            self._draw()

    def on_step(self, steps: int) -> None:
        """Update the agent's step counter (cumulative for multi-turn cases)."""
        try:
            self.steps = max(self.steps, int(steps))
        except (TypeError, ValueError):
            return
        self._draw()

    def on_tool(self, name: str, ok: bool = True) -> None:
        """Update the tool counter; called by the harness recorder."""
        self.tools += 1
        if not ok:
            self.tool_errors += 1
        if name:
            self.last_tool = str(name)
        self._draw()

    def on_stats(self, stats: dict[str, Any]) -> None:
        """Optional hook for backends that stream live token statistics."""
        if not stats:
            return
        steps = stats.get("steps")
        if steps:
            self.on_step(int(steps))
        else:
            self._draw()

    # -- rendering ---------------------------------------------------------

    def _head(self) -> str:
        suite = f"{self.suite} " if self.suite else ""
        return f"{suite}{self.index}/{self.total} {self.case.id}"

    def _status_line(self) -> str:
        bits = [self._head(), self.case.profile or "case", self.phase]
        bits.append(_clock(self._elapsed()))
        if self.steps:
            bits.append(f"step {self.steps}")
        if self.tools:
            suffix = "" if self.tools == 1 else "s"
            bits.append(f"{self.tools} tool{suffix}")
        if self.tool_errors:
            bits.append(f"{self.tool_errors} failed")
        if self.last_tool:
            bits.append(f"last {self.last_tool}")
        return "[eval] " + " | ".join(bits)

    def _draw(self) -> None:
        if not self._live or self._finished or self.phase == "judging":
            return
        line = _fit(self._status_line(), self._width - 1)
        with self._lock:
            if not self._live:
                return
            try:
                self._stream.write(_CLEAR_LINE + _paint(line, "36"))
                self._stream.flush()
                self._drawn = True
            except (OSError, ValueError):
                self._live = False

    def _clear(self) -> None:
        with self._lock:
            if not self._drawn or self._stream is None:
                return
            try:
                self._stream.write(_CLEAR_LINE)
                self._stream.flush()
            except (OSError, ValueError):
                self._live = False
            self._drawn = False

    def _emit_line(self, text: str) -> None:
        """Write a static line to the log and, when stdout is captured, the TTY."""
        print(text, flush=True)
        if self._live and not _print_is_tty():
            with self._lock:
                try:
                    self._stream.write(text + "\n")
                    self._stream.flush()
                except (OSError, ValueError):
                    self._live = False

    def _final_line(self, result: Any, error: Optional[str]) -> str:
        # Use wall time so the final line matches the live clock (workspace
        # setup, agent run, judging and report all count). The per-case report
        # keeps the agent-only duration separately.
        duration = self._elapsed()
        if result is not None:
            steps = int(getattr(result, "steps", 0) or 0)
            calls = list(getattr(result, "tool_calls", []) or [])
            tools = len(calls)
            failed = sum(1 for call in calls if not getattr(call, "ok", True))
            model = str(getattr(result, "model", "") or "").strip()
        else:
            steps = self.steps
            tools = self.tools
            failed = self.tool_errors
            model = ""

        bits = [self._head(), "ok" if not error else "FAIL", f"{duration:.1f}s"]
        if steps:
            bits.append(f"{steps} step" + ("" if steps == 1 else "s"))
        if tools:
            bits.append(f"{tools} tool" + ("" if tools == 1 else "s"))
        if failed:
            bits.append(f"{failed} failed")
        if result is not None:
            if getattr(result, "timed_out", False):
                bits.append("timeout")
            if getattr(result, "truncated", False):
                bits.append("truncated")
        if model:
            bits.append(model)
        return "[eval] " + " | ".join(bits)

    def finish(self, result: Any = None, error: Optional[str] = None) -> None:
        """Stop the live line and print one static result line."""
        if self._finished:
            return
        self._finished = True
        self._stop.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=max(1.0, self._interval * 2))
        self._clear()
        self._emit_line(self._final_line(result, error))


__all__ = ["CaseProgress"]
