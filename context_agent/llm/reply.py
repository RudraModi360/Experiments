"""Normalized chat reply returned by an LLM adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LLMReply:
    message: Dict[str, Any]
    prompt_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    # Timing reported by the backend where available (uzu fills these in).
    tokens_per_second: Optional[float] = None
    time_to_first_token: Optional[float] = None
    prefill_tokens_per_second: Optional[float] = None
    duration: Optional[float] = None
