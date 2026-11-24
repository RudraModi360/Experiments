"""Prompt budget limits derived from the model window and tool schema cost."""

from __future__ import annotations

from dataclasses import dataclass

from ..config import Config


@dataclass
class Limits:
    prompt_limit: int
    trigger: int
    clear_target: int
    keep: int


class BudgetPolicy:
    def __init__(self, cfg: Config, tools_tokens: int):
        self.cfg = cfg
        self.tools_tokens = tools_tokens

    def limits(self) -> Limits:
        usable = int((self.cfg.num_ctx - self.cfg.num_predict) * self.cfg.safety_margin)
        limit = max(2000, usable - self.tools_tokens)
        return Limits(limit, int(limit * self.cfg.trigger_ratio), int(limit * self.cfg.clear_target_ratio),
                      int(limit * self.cfg.keep_ratio))
