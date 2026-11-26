"""Rolling-summary generation, including the mechanical no-LLM digest fallback."""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Optional

from ..config import Config
from ..llm.errors import LLMError
from ..utilities.text import clip, head_tail, short_args, strip_think
from .prompts import SUMMARIZER_SYSTEM


class ContextSummarizer:
    def __init__(self, cfg: Config, llm: Any, emit: Callable[..., None]):
        self.cfg = cfg
        self.llm = llm
        self.emit = emit

    @staticmethod
    def render_old(msgs: List[Dict[str, Any]], scale: float = 1.0) -> List[str]:
        s = max(1.0, min(3.0, float(scale)))
        lines = []
        for m in msgs:
            meta = m.get("_meta") or {}
            if m["role"] == "user":
                lines.append("USER: " + head_tail(m.get("content") or "", int(2200 * s), int(500 * s)))
            elif m["role"] == "assistant":
                text = (m.get("content") or "").strip()
                calls = "; ".join(f"{c['function']['name']}({short_args(c['function'].get('arguments'), int(300 * s))})"
                                  for c in m.get("tool_calls") or [])
                lines.append("ASSISTANT: " + head_tail(text, int(1200 * s), int(200 * s)) + (f"\n  CALLS: {calls}" if calls else ""))
            elif m["role"] == "tool":
                body = meta.get("full") or m.get("content") or ""
                lines.append(f"RESULT[{m.get('tool_name', '?')}]: " + head_tail(body, int(900 * s), int(300 * s)))
        return lines

    def summarize(self, previous: str, chunk: str) -> Optional[str]:
        word_target = max(400, int(self.cfg.max_summary_chars / 10))
        prompt = (
            "Update the agent's working memory.\n\n"
            "Rules:\n"
            f"- Merge PREVIOUS MEMORY with NEW EVENTS into one updated memory (max ~{word_target} words).\n"
            "- Keep exact values that may be needed later: names, numbers, IDs, paths, URLs, commands, "
            "error messages, and the user's preferences or constraints.\n"
            "- For research/report tasks keep the data needed for the deliverable: per-entity stats, "
            "scores, dates and the source URL for each fact. State what each saved file contains so it "
            "can be re-read with read_file instead of re-fetching.\n"
            "- Record findings and decisions, not the play-by-play. Drop finished details that no longer matter.\n"
            "- Do not copy long file or web contents; state what was learned.\n"
            "- If the user changed topic, make the new topic the objective and shrink the old one to one line.\n"
            "- Use exactly these headings: ## Objective, ## Constraints & preferences, ## Progress, "
            "## Key findings, ## Open items & next step, ## Dead ends (don't repeat).\n\n"
            f"PREVIOUS MEMORY:\n{previous or '(none)'}\n\nNEW EVENTS:\n{chunk}\n\nUPDATED MEMORY:")
        try:
            reply = self.llm.chat([{"role": "system", "content": SUMMARIZER_SYSTEM},
                                   {"role": "user", "content": prompt}], None,
                                  temperature=0.0, num_predict=self.cfg.summary_tokens)
        except LLMError as exc:
            self.emit("compression", "summarizer_failed", error=str(exc)[:200])
            return None
        text = strip_think(reply.message.get("content") or "")
        text = re.sub(r"^```(?:markdown|md)?\s*|\s*```$", "", text).strip()
        if len(text) < 80:
            self.emit("compression", "summary_rejected", chars=len(text))
            return None
        if len(text) > self.cfg.max_summary_chars:
            again = self.llm.chat([{"role": "system", "content": SUMMARIZER_SYSTEM},
                                   {"role": "user", "content": "Condense to under 300 words, keep the same headings "
                                    "and all exact values:\n\n" + text}], None, temperature=0.0,
                                  num_predict=self.cfg.summary_tokens)
            shorter = strip_think(again.message.get("content") or "")
            text = shorter if 80 <= len(shorter) < len(text) else text
        return head_tail(text, int(self.cfg.max_summary_chars * 0.7), int(self.cfg.max_summary_chars * 0.3)) \
            if len(text) > self.cfg.max_summary_chars else text

    def fold(self, old: List[Dict[str, Any]], previous: str, use_llm: bool) -> str:
        scale = max(1.0, min(3.0, self.cfg.max_summary_chars / 4500.0))
        lines = self.render_old(old, scale=scale)
        chunk_chars = max(3000, int(self.cfg.num_ctx * 0.5 * 3.0) - 6500)
        chunks, cur, size = [], [], 0
        for ln in lines:
            if cur and size + len(ln) > chunk_chars:
                chunks.append("\n".join(cur))
                cur, size = [], 0
            cur.append(ln)
            size += len(ln) + 1
        if cur:
            chunks.append("\n".join(cur))
        state = previous
        for chunk in chunks:
            new = self.summarize(state, chunk) if use_llm else None
            if new is None:  # mechanical digest: lossy but never crashes and never overflows
                digest = "\n".join(clip(ln.replace("\n", " "), 140) for ln in chunk.split("\n") if ln.strip())
                state = (re.sub(r"\n## Auto-digest.*", "", state, flags=re.S) +
                         "\n## Auto-digest (summarizer unavailable)\n" + head_tail(digest, 1200, 400)).strip()
                state = head_tail(state, int(self.cfg.max_summary_chars * 0.6), int(self.cfg.max_summary_chars * 0.4))
            else:
                state = new
        return state
