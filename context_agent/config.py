"""Runtime configuration for the agent and its context budget policy."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


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
    num_ctx: int = int(os.environ.get("AGENT_NUM_CTX", "131072"))  # 128k window (Qwen3.5-9B-M)
    num_predict: int = int(os.environ.get("AGENT_NUM_PREDICT", "8192"))  # Qwen 9B reasons a lot; small budgets leave no room for the answer
    temperature: float = 0.2
    request_timeout: float = 300.0

    # --- budget policy (fractions of the usable prompt space) ---
    safety_margin: float = 0.92       # token counting is approximate; keep 8% headroom
    trigger_ratio: float = 0.75       # start cleaning above this
    clear_target_ratio: float = 0.62  # step 3 aims for this
    keep_ratio: float = 0.35          # step 4 leaves roughly this much recent history
    keep_recent_units: int = 4        # newest tool exchanges are never cleared in step 3

    # --- per-item caps ---
    max_tool_chars: int = 5000        # max chars of one tool result kept in context
    max_unit_ratio: float = 0.30      # all results of one model step share this much of the prompt
    max_user_ratio: float = 0.25      # a user message above this is spilled to a file
    max_summary_chars: int = 4500
    max_ledger_chars: int = 4500
    max_notes_chars: int = 3000
    summary_tokens: int = 900

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
