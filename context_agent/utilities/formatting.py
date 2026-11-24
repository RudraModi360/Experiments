"""Human-readable number formatting and terminal colors."""

from __future__ import annotations

import os
import sys
from typing import Optional


def color_enabled() -> bool:
    return (
        sys.stdout.isatty()
        and os.environ.get("NO_COLOR") is None
        and os.environ.get("TERM") != "dumb"
    )


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if color_enabled() else text


def ok(text: str) -> str:
    return paint(text, "32")  # green


def fail(text: str) -> str:
    return paint(text, "31")  # red


def hint(text: str) -> str:
    return paint(text, "36")  # cyan


def warn(text: str) -> str:
    return paint(text, "33")  # yellow


def bold(text: str) -> str:
    return paint(text, "1")


def dim(text: str) -> str:
    return paint(text, "2")


def format_tool_stats(stats: Optional[dict]) -> str:
    """Build the per-turn '[tools] N calls | X ok | Y failed | Z blocked' line."""
    if not stats:
        return ""
    calls = int(stats.get("calls") or 0)
    if not calls:
        return ""
    good = int(stats.get("ok") or 0)
    failed = int(stats.get("failed") or 0)
    blocked = int(stats.get("blocked") or 0)
    bits = [f"{calls} call" + ("" if calls == 1 else "s"), ok(f"{good} ok")]
    if failed:
        bits.append(fail(f"{failed} failed"))
    if blocked:
        bits.append(warn(f"{blocked} blocked"))
    return "[tools] " + " | ".join(bits)


def format_stats(stats: Optional[dict], compact: bool = False) -> str:
    """Build the '[stats] ...' line from token/timing fields (shared live + final).

    ``compact`` shortens labels so the live line fits on one terminal row; the
    content (out/in tokens, tok/s, TTFT, prefill speed, gen time) is identical.
    """
    if not stats:
        return ""
    bits = []
    if stats.get("output_tokens"):
        bits.append(f"{stats['output_tokens']} out tok")
    if stats.get("prompt_tokens"):
        bits.append(f"{stats['prompt_tokens']} in tok")
    if stats.get("tokens_per_second") is not None:
        bits.append(f"{stats['tokens_per_second']:.1f} tok/s")
    if stats.get("time_to_first_token") is not None:
        bits.append(f"TTFT {stats['time_to_first_token']:.2f}s")
    if stats.get("prefill_tokens_per_second") is not None:
        speed = f"{stats['prefill_tokens_per_second']:.0f}"
        bits.append(f"prefill {speed}" if compact else f"prefill {speed} tok/s")
    if stats.get("duration"):
        bits.append(f"gen {stats['duration']:.1f}s")
    if not bits:
        return ""
    line = "[stats] " + " | ".join(bits)
    return line


def fmt_tokens(n: int) -> str:
    """Compact token count for budget lines: 987, 12.3k, 1.2M."""
    n = int(n or 0)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def fmt_size(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{int(size)}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{n}B"
