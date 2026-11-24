"""Before/after telemetry for context-budget maintenance passes.

Every time the agent has to make room in the prompt, one `MaintainPass` records
the budget it started from and each action taken (compress / mask / emergency)
with token counts before and after.  This makes it possible to tell *real*
compression (folding old units into the rolling summary) from mere masking
(clearing or stubbing old tool results), and to spot repeated thrash across a
long run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from ..utilities.formatting import dim, fail, fmt_tokens, ok, warn


@dataclass
class MaintainPass:
    tokens_before: int
    limit: int
    trigger: int
    clear_target: int
    window: int
    reserve_out: int
    tools: int
    forced: bool = False
    actual_before: Optional[int] = None
    started: datetime = field(default_factory=datetime.now)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    tokens_after: Optional[int] = None
    duration_ms: int = 0

    # ------------------------------------------------------------------ recorders
    def compressed(self, folded: int, kept: int, before: int, after: int,
                   summary_chars: int, llm: bool) -> None:
        self.actions.append({"kind": "compress", "folded": folded, "kept": kept,
                             "before": before, "after": after,
                             "summary_chars": summary_chars, "llm": bool(llm)})

    def masked(self, count: int, before: int, after: int) -> None:
        self.actions.append({"kind": "mask", "count": count, "before": before, "after": after})

    def emergency(self, before: int, after: int) -> None:
        self.actions.append({"kind": "emergency", "before": before, "after": after})

    def skipped(self, reason: str) -> None:
        self.actions.append({"kind": "skip", "reason": reason})

    # ------------------------------------------------------------------ rendering
    def _head(self) -> str:
        prompt = self.tokens_before + self.tools
        bits = [f"{dim('prompt')} {fmt_tokens(prompt)}",
                f"{dim('view')} {fmt_tokens(self.tokens_before)} + {dim('tools')} {fmt_tokens(self.tools)}"]
        if self.forced:
            bits.append(warn("forced"))
        bits.append(f"{dim('trigger')} {fmt_tokens(self.trigger)}")
        return "[ctx] " + " | ".join(bits)

    def render(self) -> str:
        bits = [self._head()]
        for action in self.actions:
            kind = action.get("kind")
            if kind == "compress":
                delta = max(0, action["before"] - action["after"])
                bits.append(f"{ok('compress')} {action['folded']} msgs "
                            f"{fmt_tokens(action['before'])}→{fmt_tokens(action['after'])} "
                            f"(-{fmt_tokens(delta)})")
            elif kind == "mask":
                delta = max(0, action["before"] - action["after"])
                bits.append(f"{warn('mask')} {action['count']} results "
                            f"{fmt_tokens(action['before'])}→{fmt_tokens(action['after'])} "
                            f"(-{fmt_tokens(delta)})")
            elif kind == "emergency":
                delta = max(0, action["before"] - action["after"])
                bits.append(f"{fail('emergency')} {fmt_tokens(action['before'])}→"
                            f"{fmt_tokens(action['after'])} (-{fmt_tokens(delta)})")
            elif kind == "skip":
                bits.append(dim(f"skip {action.get('reason', '')}"))
        if len(bits) == 1:
            bits.append(dim("no action"))
        bits.append(dim(f"{self.duration_ms / 1000:.1f}s"))
        return " | ".join(bits)

    # ------------------------------------------------------------------ storage
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.started.isoformat(timespec="seconds"),
            "tokens_before": self.tokens_before,
            "tokens_after": self.tokens_after if self.tokens_after is not None else self.tokens_before,
            "limit": self.limit,
            "trigger": self.trigger,
            "clear_target": self.clear_target,
            "window": self.window,
            "reserve_out": self.reserve_out,
            "tools": self.tools,
            "forced": self.forced,
            "actual_before": self.actual_before,
            "duration_ms": self.duration_ms,
            "actions": list(self.actions),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MaintainPass":
        started = datetime.now()
        try:
            started = datetime.fromisoformat(str(data.get("ts")))
        except (TypeError, ValueError):
            pass
        return cls(
            tokens_before=int(data.get("tokens_before") or 0),
            limit=int(data.get("limit") or 0),
            trigger=int(data.get("trigger") or 0),
            clear_target=int(data.get("clear_target") or 0),
            window=int(data.get("window") or 0),
            reserve_out=int(data.get("reserve_out") or 0),
            tools=int(data.get("tools") or 0),
            forced=bool(data.get("forced")),
            actual_before=data.get("actual_before"),
            started=started,
            actions=list(data.get("actions") or []),
            tokens_after=data.get("tokens_after"),
            duration_ms=int(data.get("duration_ms") or 0),
        )


class ContextTelemetry:
    """Keep the current session's passes in memory and persist them as JSONL."""

    def __init__(self, cfg: Any, sink: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.cfg = cfg
        self.sink = sink
        self.passes: List[MaintainPass] = []
        self.totals = self._empty()

    @staticmethod
    def _empty() -> Dict[str, Any]:
        return {"passes": 0, "compress_passes": 0, "mask_passes": 0, "emergency_passes": 0,
                "mask_only": 0, "folded_messages": 0, "masked_results": 0,
                "compressed_tokens": 0, "masked_tokens": 0, "last": None}

    def reset(self) -> None:
        self.passes = []
        self.totals = self._empty()

    def load(self, records: List[Dict[str, Any]]) -> None:
        self.reset()
        for record in records:
            try:
                self.passes.append(MaintainPass.from_dict(record))
            except (TypeError, ValueError):
                continue
        del self.passes[:-100]
        for item in self.passes:
            self._count(item)

    def _count(self, item: MaintainPass) -> None:
        totals = self.totals
        totals["passes"] += 1
        kinds = [a.get("kind") for a in item.actions]
        if "compress" in kinds:
            totals["compress_passes"] += 1
            for action in item.actions:
                if action.get("kind") == "compress":
                    totals["folded_messages"] += int(action.get("folded") or 0)
                    totals["compressed_tokens"] += max(0, int(action.get("before") or 0)
                                                       - int(action.get("after") or 0))
        if "mask" in kinds:
            totals["mask_passes"] += 1
            for action in item.actions:
                if action.get("kind") == "mask":
                    totals["masked_results"] += int(action.get("count") or 0)
                    totals["masked_tokens"] += max(0, int(action.get("before") or 0)
                                                   - int(action.get("after") or 0))
        if "emergency" in kinds:
            totals["emergency_passes"] += 1
        if "mask" in kinds and "compress" not in kinds:
            totals["mask_only"] += 1
        totals["last"] = item

    def record(self, item: MaintainPass) -> None:
        self.passes.append(item)
        del self.passes[:-100]
        self._count(item)
        if self.sink:
            try:
                self.sink(item.to_dict())
            except Exception:
                pass
        if getattr(self.cfg, "show_context", True):
            print(item.render(), flush=True)

    def recent(self, count: int = 6) -> List[MaintainPass]:
        return self.passes[-count:]

    def summary(self) -> str:
        totals = self.totals
        if not totals["passes"]:
            return "no maintenance passes yet"
        return (f"{totals['passes']} passes | "
                f"compress {totals['compress_passes']} "
                f"({totals['folded_messages']} msgs, -{fmt_tokens(totals['compressed_tokens'])}) | "
                f"mask {totals['mask_passes']} "
                f"({totals['masked_results']} results, -{fmt_tokens(totals['masked_tokens'])}) | "
                f"emergency {totals['emergency_passes']} | mask-only {totals['mask_only']}")
