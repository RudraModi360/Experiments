"""Approximate, multilingual-aware token counting that self-corrects upward."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


class TokenCounter:
    def __init__(self, chars_per_token: float = 3.4):
        self.cpt = chars_per_token
        self.scale = 1.0

    def text(self, s: str) -> int:
        if not s:
            return 0
        non_ascii = sum(1 for c in s if ord(c) > 127)
        ascii_n = len(s) - non_ascii
        return int((ascii_n / self.cpt + non_ascii * 1.3) * self.scale) + 1

    def message(self, m: Dict[str, Any]) -> int:
        n = self.text(str(m.get("content") or "")) + 6
        if m.get("tool_calls"):
            n += self.text(json.dumps(m["tool_calls"], ensure_ascii=False, default=str))
        return n

    def calibrate(self, estimated: int, actual: Optional[int]) -> None:
        """Only ever raises the scale: Ollama's prompt cache can make `actual` look too small."""
        if not actual or estimated < 500:
            return
        ratio = actual / estimated
        if 1.0 < ratio <= 2.0:
            self.scale = min(1.8, self.scale * (1 + 0.3 * (ratio - 1)))
