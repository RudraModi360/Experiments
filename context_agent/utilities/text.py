"""Small text-shaping helpers shared by the context engine and the tools."""

from __future__ import annotations

import json
import re
from typing import Any

_THINK_RE = re.compile(r"<think>.*?</think>", re.S | re.I)


def strip_think(text: str) -> str:
    text = _THINK_RE.sub("", text or "")
    if "</think>" in text.lower():
        text = re.split(r"</think>", text, flags=re.I)[-1]
    return text.strip()


def head_tail(text: str, head: int, tail: int) -> str:
    if len(text) <= head + tail:
        return text
    omitted = len(text) - head - tail
    return text[:head] + f"\n...[{omitted} chars omitted]...\n" + (text[-tail:] if tail else "")


def clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: max(0, limit - 1)] + "…"


def short_args(args: Any, limit: int = 120) -> str:
    try:
        raw = json.dumps(args, ensure_ascii=False, default=str)
    except Exception:
        raw = str(args)
    return clip(raw, limit)


def around(line: str, pos: int, width: int = 240) -> str:
    if len(line) <= width:
        return line
    start = max(0, pos - width // 2)
    end = min(len(line), start + width)
    return ("…" if start else "") + line[start:end] + ("…" if end < len(line) else "")
