"""Cross-run context report: compression vs masking, and re-fetch patterns.

Usage::

    python -m context_agent.context.report
    python -m context_agent.context.report --session 20261123-122422-7bc7
    python -m context_agent.context.report --home /custom/agent/home
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from typing import Any, Dict, List, Tuple

from ..config import Config
from ..utilities.formatting import fmt_tokens


def _read_json(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _read_events(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError:
        return []
    out: List[Dict[str, Any]] = []
    for line in lines:
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if isinstance(item, dict):
            out.append(item)
    return out


def _call_counts(history: List[Dict[str, Any]]) -> Tuple[int, int, int]:
    calls: Counter = Counter()
    for msg in history:
        for call in msg.get("tool_calls") or []:
            fn = call.get("function") or {}
            calls[(fn.get("name") or "?", json.dumps(fn.get("arguments"), sort_keys=True, default=str))] += 1
    repeats = sum(count - 1 for count in calls.values() if count > 1)
    web_repeats = sum(count - 1 for (name, _), count in calls.items()
                      if count > 1 and name in ("web_search", "fetch_url"))
    return len(calls), repeats, web_repeats


def _refetch_after_mask(history: List[Dict[str, Any]]) -> int:
    """Count live tool results whose signature was already cleared/stubbed."""
    masked, repeats = set(), 0
    for msg in history:
        if msg.get("role") != "tool":
            continue
        meta = msg.get("_meta") or {}
        sig = meta.get("sig")
        if not sig:
            continue
        if meta.get("cleared") or meta.get("stubbed"):
            masked.add(sig)
        elif sig in masked:
            repeats += 1
    return repeats


def inspect(root: str, sid: str) -> Dict[str, Any]:
    directory = os.path.join(root, sid)
    state = _read_json(os.path.join(directory, "state.json"))
    events = _read_events(os.path.join(directory, "context_events.jsonl"))
    history = state.get("history") or []
    tools = sum(1 for m in history if m.get("role") == "tool")
    stubbed = sum(1 for m in history if (m.get("_meta") or {}).get("stubbed"))
    cleared = sum(1 for m in history if (m.get("_meta") or {}).get("cleared"))
    total_calls, repeats, web_repeats = _call_counts(history)
    refetch = _refetch_after_mask(history)
    kinds = [a.get("kind") for event in events for a in (event.get("actions") or [])]
    compress = kinds.count("compress")
    mask = kinds.count("mask")
    emergency = kinds.count("emergency")
    folded = sum(int(a.get("folded") or 0) for event in events for a in (event.get("actions") or [])
                 if a.get("kind") == "compress")
    masked = sum(int(a.get("count") or 0) for event in events for a in (event.get("actions") or [])
                 if a.get("kind") == "mask")
    if events:
        if compress == 0 and mask and refetch:
            verdict = "MASK-THRASH (re-fetch after masking)"
        elif compress and not mask:
            verdict = "COMPRESS-OK"
        elif compress and mask:
            verdict = "MIXED"
        elif not kinds:
            verdict = "no-ops"
        else:
            verdict = "EMERGENCY"
    elif stubbed or cleared or repeats:
        verdict = "OLD-RUN (mask evidence only)"
    else:
        verdict = "quiet"
    return {
        "sid": sid, "model": state.get("model") or "", "messages": len(history), "tools": tools,
        "stubbed": stubbed, "cleared": cleared, "calls": total_calls, "repeats": repeats,
        "web_repeats": web_repeats, "refetch": refetch, "passes": len(events),
        "compress": compress, "mask": mask, "emergency": emergency, "folded": folded,
        "masked": masked, "summary_chars": len(state.get("state", {}).get("summary") or ""),
        "verdict": verdict,
    }


def report(root: str, only: str | None = None) -> List[Dict[str, Any]]:
    try:
        names = sorted(os.listdir(root), reverse=True)
    except OSError:
        names = []
    rows = []
    for name in names:
        if only and name != only:
            continue
        if not os.path.isfile(os.path.join(root, name, "state.json")):
            continue
        rows.append(inspect(root, name))
    if not rows:
        print(f"No sessions found in {root}")
        return rows

    print(f"{'session':24} {'msg':>4} {'tool':>4} {'pass':>4} {'comp':>4} {'mask':>4} "
          f"{'fold':>5} {'masked':>6} {'re-fetch':>8}  verdict")
    for row in rows:
        print(f"{row['sid']:24} {row['messages']:4} {row['tools']:4} {row['passes']:4} "
              f"{row['compress']:4} {row['mask']:4} {fmt_tokens(row['folded']):>5} "
              f"{row['masked']:6} {row['refetch'] + row['repeats']:8}  {row['verdict']}")

    passes = sum(r["passes"] for r in rows)
    compress = sum(r["compress"] for r in rows)
    mask = sum(r["mask"] for r in rows)
    print(f"\n{len(rows)} sessions | {passes} passes | compress {compress} | mask {mask} | "
          f"re-fetch repeats {sum(r['refetch'] for r in rows)} | "
          f"repeated calls {sum(r['repeats'] for r in rows)}")
    print("compress = old units folded into SESSION MEMORY (knowledge kept); "
          "mask = old tool output stubbed/cleared (must be re-read or re-fetched).")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze context compression/masking across sessions")
    parser.add_argument("--home", default=Config().home, help="agent home directory")
    parser.add_argument("--session", help="only inspect this session id")
    args = parser.parse_args()
    report(os.path.join(args.home, "sessions"), args.session)


if __name__ == "__main__":
    main()
