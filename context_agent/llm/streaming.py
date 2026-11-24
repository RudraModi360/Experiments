"""Streaming helpers for model output.

The Ollama adapter emits raw content deltas.  `ThinkFilter` removes
``<think>...</think>`` blocks even when a tag is split across chunks, and
`StreamPrinter` writes the visible text to the terminal as it arrives.
"""

from __future__ import annotations

import shutil
import time
from typing import Any, Callable, Dict, List, Optional

from ..utilities.formatting import color_enabled, format_stats, hint

TokenCallback = Callable[[str], None]

_OPEN = "<think>"
_CLOSE = "</think>"


def _held_suffix(text: str, tag: str) -> int:
    """Length of the longest suffix of *text* that is a prefix of *tag*."""
    for size in range(min(len(text), len(tag) - 1), 0, -1):
        if text[-size:].lower() == tag[:size].lower():
            return size
    return 0


class ThinkFilter:
    """Incrementally remove think blocks from a stream of text deltas."""

    def __init__(self) -> None:
        self._buffer = ""
        self._in_think = False

    def feed(self, text: str) -> str:
        self._buffer += text or ""
        out: List[str] = []
        while self._buffer:
            if self._in_think:
                lower = self._buffer.lower()
                index = lower.find(_CLOSE)
                if index >= 0:
                    self._buffer = self._buffer[index + len(_CLOSE):]
                    self._in_think = False
                    continue
                keep = _held_suffix(self._buffer, _CLOSE)
                self._buffer = self._buffer[-keep:] if keep else ""
                break
            lower = self._buffer.lower()
            index = lower.find(_OPEN)
            if index >= 0:
                out.append(self._buffer[:index])
                self._buffer = self._buffer[index + len(_OPEN):]
                self._in_think = True
                continue
            keep = _held_suffix(self._buffer, _OPEN)
            if keep:
                out.append(self._buffer[:-keep])
                self._buffer = self._buffer[-keep:]
            else:
                out.append(self._buffer)
                self._buffer = ""
            break
        return "".join(out)

    def flush(self) -> str:
        """Return held text that is safe to print, or drop an open think block."""
        if self._in_think:
            self._buffer = ""
            return ""
        text, self._buffer = self._buffer, ""
        return text


class LiveTokenMeter:
    """Keep a live ``[stats]`` telemetry line pinned just below the streamed text.

    The status is the last line on screen: new text is written above it and the
    status is redrawn underneath, so it behaves like the status area in coding
    CLIs instead of scrolling away or repeating.  Feeds off the backend's
    per-chunk stats, so the numbers are the real ones uzu reports.  Disabled on
    non-TTY output.

    Only relative cursor motion is used (never absolute rows), so it also works
    once the stream reaches the bottom of the terminal and starts scrolling.
    """

    def __init__(self, write: Optional[Callable[[str], None]] = None) -> None:
        self._write = write or (lambda text: print(text, end="", flush=True))
        self._enabled = color_enabled()
        self._width = max(20, shutil.get_terminal_size(fallback=(80, 24)).columns)
        self._stats: Dict[str, Any] = {}
        self._col = 0          # visual column of the cursor in the text
        self._at_start = True  # cursor is at column 0 (after a newline)
        self._drawn = False
        self._offset = 0       # 0: status shares the text row, 1: next row
        self._last_draw = 0.0
        self._min_interval = 0.04  # cap redraws at ~25 fps

    @property
    def enabled(self) -> bool:
        return self._enabled

    def begin(self) -> None:
        """Reset for a fresh reply; the status appears with the first stats."""
        self._erase()
        self._col = 0
        self._at_start = True
        self._stats = {}

    def _status_text(self) -> str:
        line = format_stats(self._stats)
        if not line:
            return ""
        limit = max(10, self._width - 1)
        if len(line) > limit:
            line = line[: limit - 1] + "…"
        return hint(line)

    def _restore_col(self) -> None:
        if self._col:
            self._write(f"\033[{self._col}C")

    def _erase(self) -> None:
        if not self._drawn:
            return
        if self._offset == 1:
            self._write("\033[1B")      # down to the status row
            self._write("\r\033[2K")    # clear it
            self._write("\033[1A")      # back up to the text row
            self._restore_col()
        else:
            self._write("\r\033[2K")    # status shares the text row
        self._drawn = False

    def _draw(self) -> None:
        if not self._enabled:
            return
        text = self._status_text()
        if not text:
            return
        self._erase()
        if self._at_start:
            # Cursor is on a fresh line: put the status there, then return.
            self._write(text)
            self._write("\r")
            self._restore_col()
            self._offset = 0
        else:
            # Move to the next line, draw the status, then return to the text.
            # If that line is the last row the terminal scrolls, which moves
            # the text up exactly one row - the move back up still lands on it.
            self._write("\r\n")
            self._write(text)
            self._write("\033[1A\r")
            self._restore_col()
            self._offset = 1
        self._drawn = True
        self._last_draw = time.monotonic()

    def on_stats(self, stats: Dict[str, Any]) -> None:
        """Update the live telemetry from the backend's latest stats snapshot."""
        if not self._enabled or not any(stats.values()):
            return
        self._stats = stats
        now = time.monotonic()
        if self._drawn and now - self._last_draw < self._min_interval:
            return
        self._draw()

    def before_text(self) -> None:
        """Erase the status so streamed text does not overwrite it."""
        self._erase()

    def after_text(self, delta: str) -> None:
        """Advance the tracked cursor over *delta* and redraw the status."""
        if not delta:
            return
        for ch in delta:
            if ch == "\n":
                self._col = 0
                self._at_start = True
            else:
                if self._col >= self._width:
                    self._col = 0
                    self._at_start = False
                self._col += 1
                self._at_start = False
        if self._col >= self._width:
            self._col = self._width - 1
        self._draw()

    def finish(self) -> None:
        """Remove the live status; the caller prints the final stats line."""
        self._erase()

    def reset(self) -> None:
        """Finish one model reply and get ready for the next one."""
        self.begin()


class StreamPrinter:
    """Write visible model deltas to a stream and remember what was shown."""

    def __init__(self, write: Optional[Callable[[str], None]] = None,
                 meter: Optional[LiveTokenMeter] = None) -> None:
        self._write = write or (lambda text: print(text, end="", flush=True))
        self._filter = ThinkFilter()
        self._meter = meter
        self.text = ""
        self.visible = False

    def feed(self, delta: str) -> None:
        visible = self._filter.feed(delta)
        if not visible:
            return
        self.text += visible
        self.visible = True
        if self._meter:
            self._meter.before_text()
        self._write(visible)
        if self._meter:
            self._meter.after_text(visible)

    def finish(self) -> None:
        visible = self._filter.flush()
        if not visible:
            return
        self.text += visible
        self.visible = True
        if self._meter:
            self._meter.before_text()
        self._write(visible)
        if self._meter:
            self._meter.after_text(visible)
