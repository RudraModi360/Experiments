"""Runtime configuration for the agent and its context budget policy."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Optional, Set, Union


def parse_ctx_size(value: Union[int, str]) -> int:
    """Parse context window sizes like 131072, '32k', '128K', '1m', or '1M'."""
    if isinstance(value, int):
        return max(4096, value)
    raw = str(value).strip().lower().replace("_", "").replace(",", "")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([km])?", raw)
    if not m:
        raise ValueError(f"invalid context size: {value!r} (expected e.g. 32k, 128k, 256k, 1m, or integer)")
    num = float(m.group(1))
    unit = m.group(2)
    if unit == "k":
        num *= 1024
    elif unit == "m":
        num *= 1024 * 1024
    return max(4096, int(num))


def _env_int(name: str) -> Optional[int]:
    val = os.environ.get(name, "").strip()
    return parse_ctx_size(val) if val else None


@dataclass
class Config:
    model: str = os.environ.get("AGENT_MODEL", "trymirai/Qwen3.5-9B-M")
    host: Optional[str] = os.environ.get("OLLAMA_HOST") or None
    provider: str = (
        os.environ.get("AGENT_PROVIDER")
        or ("llama-cpp" if (os.environ.get("AGENT_BASE_URL") or os.environ.get("LLAMA_CPP_BASE_URL")) else "mirai")
    ).strip().lower()
    base_url: Optional[str] = os.environ.get("AGENT_BASE_URL") or os.environ.get("LLAMA_CPP_BASE_URL") or None
    api_key: Optional[str] = os.environ.get("AGENT_API_KEY") or os.environ.get("LLAMA_CPP_API_KEY") or None
    num_ctx: int = parse_ctx_size(os.environ.get("AGENT_NUM_CTX", "131072"))  # 128k window default
    num_predict: Optional[int] = _env_int("AGENT_NUM_PREDICT")
    temperature: float = 0.2
    request_timeout: float = 300.0

    # --- budget policy (fractions of the usable prompt space) ---
    safety_margin: float = 0.92       # token counting is approximate; keep 8% headroom
    trigger_ratio: float = 0.75       # start cleaning above this
    clear_target_ratio: float = 0.62  # step 3 aims for this
    keep_ratio: float = 0.35          # step 4 leaves roughly this much recent history
    keep_recent_units: Optional[int] = None  # newest tool exchanges never cleared (auto-scaled)

    # --- per-item caps (None = auto-derived from num_ctx in apply_context_scale) ---
    max_tool_chars: Optional[int] = None
    max_unit_ratio: float = 0.30      # all results of one model step share this much of the prompt
    max_user_ratio: float = 0.25      # a user message above this is spilled to a file
    max_summary_chars: Optional[int] = None
    max_ledger_chars: Optional[int] = None
    max_notes_chars: Optional[int] = None
    max_note_chars: Optional[int] = None
    max_plan_chars: Optional[int] = None
    summary_tokens: Optional[int] = None
    read_default_lines: Optional[int] = None
    file_tracker_limit: Optional[int] = None
    workspace_snapshot_entries: Optional[int] = None
    clear_min_chars: Optional[int] = None
    clear_arg_chars: Optional[int] = None
    max_saved_items: Optional[int] = None
    max_urls_items: Optional[int] = None

    # --- loop control ---
    max_steps_per_turn: int = 25
    loop_warn: int = 3
    loop_stop: int = 5

    # --- storage ---
    home: str = os.environ.get("AGENT_HOME", os.path.join(os.path.expanduser("~"), ".intelligent_agent"))
    retention_days: int = 14

    # --- tools ---
    bash_timeout: int = 30            # default seconds for one bash command
    bash_timeout_max: int = 300       # hard cap on a requested timeout
    bash_max_output_bytes: int = 1_000_000  # capture cap; larger output is truncated
    web_timeout: int = 10
    fetch_timeout: int = 20
    fetch_max_bytes: int = 3_000_000
    verbose: bool = True
    show_tools: bool = True          # always show tool calls/results (even with --quiet)
    show_context: bool = True        # always show context budget passes (even with --quiet)

    _explicit: Set[str] = field(default_factory=set, init=False, repr=False, compare=False)

    _DERIVED_FIELDS = (
        "num_predict", "keep_recent_units", "max_tool_chars", "max_summary_chars",
        "max_ledger_chars", "max_notes_chars", "max_note_chars", "max_plan_chars",
        "summary_tokens", "read_default_lines", "file_tracker_limit",
        "workspace_snapshot_entries", "clear_min_chars", "clear_arg_chars",
        "max_saved_items", "max_urls_items",
    )

    def __post_init__(self) -> None:
        self.num_ctx = parse_ctx_size(self.num_ctx)
        for name in self._DERIVED_FIELDS:
            if getattr(self, name) is not None:
                self._explicit.add(name)
        self.apply_context_scale()

    def apply_context_scale(self, num_ctx: Optional[Union[int, str]] = None) -> None:
        """Recompute all non-explicit budgets proportionally from ``num_ctx``."""
        if num_ctx is not None:
            self.num_ctx = parse_ctx_size(num_ctx)
        ctx = max(4096, int(self.num_ctx))

        def _set(name: str, value: int) -> None:
            if name not in self._explicit:
                setattr(self, name, value)

        # Output reserve: <= 25% of small windows, 8k at 32k-128k, 16k at 256k+
        if ctx >= 262_144:
            pred = 16_384
        elif ctx >= 32_768:
            pred = 8_192
        else:
            pred = max(1024, min(8_192, int(ctx * 0.25)))
        _set("num_predict", pred)

        usable_prompt = max(2000, int((ctx - int(self.num_predict or pred)) * self.safety_margin) - 2000)
        _set("max_tool_chars", max(4_000, min(48_000, int(usable_prompt * 0.10 * 3.2))))

        if ctx >= 262_144:
            _set("keep_recent_units", 16)
            _set("max_summary_chars", 16_000)
            _set("summary_tokens", 3_000)
            _set("max_ledger_chars", 14_000)
            _set("max_notes_chars", 16_000)
            _set("max_note_chars", 1_500)
            _set("max_plan_chars", 3_000)
            _set("read_default_lines", 800)
            _set("file_tracker_limit", 40)
            _set("workspace_snapshot_entries", 120)
            _set("clear_min_chars", 3_000)
            _set("clear_arg_chars", 3_000)
            _set("max_saved_items", 20)
            _set("max_urls_items", 24)
        elif ctx >= 98_304:
            _set("keep_recent_units", 8)
            _set("max_summary_chars", 10_000)
            _set("summary_tokens", 2_000)
            _set("max_ledger_chars", 10_000)
            _set("max_notes_chars", 10_000)
            _set("max_note_chars", 1_200)
            _set("max_plan_chars", 2_400)
            _set("read_default_lines", 450)
            _set("file_tracker_limit", 24)
            _set("workspace_snapshot_entries", 80)
            _set("clear_min_chars", 1_500)
            _set("clear_arg_chars", 1_500)
            _set("max_saved_items", 16)
            _set("max_urls_items", 20)
        elif ctx >= 24_576:
            _set("keep_recent_units", 4)
            _set("max_summary_chars", 4_500)
            _set("summary_tokens", 900)
            _set("max_ledger_chars", 4_500)
            _set("max_notes_chars", 3_000)
            _set("max_note_chars", 500)
            _set("max_plan_chars", 1_500)
            _set("read_default_lines", 250)
            _set("file_tracker_limit", 12)
            _set("workspace_snapshot_entries", 40)
            _set("clear_min_chars", 500)
            _set("clear_arg_chars", 600)
            _set("max_saved_items", 8)
            _set("max_urls_items", 10)
        else:
            _set("keep_recent_units", 3)
            _set("max_summary_chars", 3_500)
            _set("summary_tokens", 700)
            _set("max_ledger_chars", 3_500)
            _set("max_notes_chars", 2_500)
            _set("max_note_chars", 500)
            _set("max_plan_chars", 1_200)
            _set("read_default_lines", 150)
            _set("file_tracker_limit", 10)
            _set("workspace_snapshot_entries", 30)
            _set("clear_min_chars", 500)
            _set("clear_arg_chars", 600)
            _set("max_saved_items", 6)
            _set("max_urls_items", 8)
