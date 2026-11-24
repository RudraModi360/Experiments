"""Structured trace of context-engine decisions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ContextTraceEvent:
    stage: str
    action: str
    details: Dict[str, Any] = field(default_factory=dict)


class ContextTrace:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.events: List[ContextTraceEvent] = []

    def append(self, stage: str, action: str, **details: Any) -> None:
        """Record an event without printing it (routine budget bookkeeping)."""
        self.events.append(ContextTraceEvent(stage, action, details))
        del self.events[:-500]

    def emit(self, stage: str, action: str, **details: Any) -> None:
        self.append(stage, action, **details)
        if self.verbose:
            print(f"[ctx:{stage}] {action} {json.dumps(details, ensure_ascii=False, default=str)}", flush=True)
