"""Pure helpers over the conversation message list."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def public_message(m: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(m)
    if "_meta" in out:
        out["_meta"] = {k: v for k, v in out["_meta"].items() if k != "full"}
    return out


def clean_message(m: Dict[str, Any]) -> Dict[str, Any]:
    out = {"role": m["role"], "content": m.get("content") or ""}
    if m.get("tool_calls"):
        out["tool_calls"] = m["tool_calls"]
    if m["role"] == "tool" and m.get("tool_name"):
        out["tool_name"] = m["tool_name"]
    return out


def message_units(history: List[Dict[str, Any]]) -> List[Tuple[int, int]]:
    """Indivisible groups: a user msg, a final assistant msg, or assistant(tool_calls)+its results."""
    out, h, i = [], history, 0
    while i < len(h):
        if h[i]["role"] == "assistant" and h[i].get("tool_calls"):
            end = min(len(h), i + 1 + len(h[i]["tool_calls"]))
            out.append((i, end))
            i = end
        else:
            out.append((i, i + 1))
            i += 1
    return out


def stub_message(m: Dict[str, Any], text: str) -> None:
    m.setdefault("_meta", {})["stubbed"] = True
    m["content"] = text
