"""Tool result envelope and tool-level error type."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


class ToolError(Exception):
    pass


@dataclass
class ToolResult:
    text: str
    ok: bool = True
    meta: Dict[str, Any] = field(default_factory=dict)
    capped: bool = False  # already bounded by the tool itself; do not spill
