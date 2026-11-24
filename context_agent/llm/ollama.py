"""Thin Ollama chat adapter. num_ctx is always sent explicitly."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from ..config import Config
from .errors import LLMError
from .reply import LLMReply
from .streaming import TokenCallback


def _plain(obj: Any) -> Any:
    if obj is None or isinstance(obj, (dict, list, str, int, float, bool)):
        return obj
    dump = getattr(obj, "model_dump", None)
    if callable(dump):
        return dump()
    try:
        return dict(obj)
    except Exception:
        return obj


def _field(obj: Any, key: str) -> Any:
    try:
        return obj[key]
    except Exception:
        return getattr(obj, key, None)


class OllamaLLM:
    """Thin wrapper over the `ollama` python library. num_ctx is always sent explicitly."""

    supports_streaming = True

    def __init__(self, cfg: Config):
        self.cfg = cfg
        try:
            import ollama  # noqa: WPS433 (lazy import keeps the module importable without it)
        except ImportError as exc:
            raise LLMError("The 'ollama' python library is missing. Install it: pip install ollama") from exc
        kwargs: Dict[str, Any] = {"timeout": cfg.request_timeout}
        if cfg.host:
            kwargs["host"] = cfg.host
        self._client = ollama.Client(**kwargs)

    def _request(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]], *,
                 temperature: Optional[float], num_predict: Optional[int], stream: bool) -> Any:
        options = {
            "num_ctx": self.cfg.num_ctx,
            "num_predict": num_predict or self.cfg.num_predict,
            "temperature": self.cfg.temperature if temperature is None else temperature,
        }
        kwargs: Dict[str, Any] = {"model": self.cfg.model, "messages": messages, "options": options,
                                  "stream": stream}
        if tools:
            kwargs["tools"] = tools
        for attempt in range(2):
            try:
                return self._client.chat(**kwargs)
            except Exception as exc:  # network blips, model loading, etc.
                if "does not support tools" in str(exc).lower():
                    raise LLMError(f"Model '{self.cfg.model}' does not support tool calling.") from exc
                if attempt == 0:
                    time.sleep(1.0)
                    continue
                raise LLMError(f"Ollama call failed: {exc}") from exc
        raise LLMError("Ollama call failed after retry")  # pragma: no cover

    @staticmethod
    def _normalize_calls(raw_calls: Any) -> List[Dict[str, Any]]:
        calls = []
        for call in raw_calls or []:
            call = _plain(call) or {}
            fn = _plain(call.get("function")) or {}
            args = fn.get("arguments")
            if not isinstance(args, (dict, str)):
                try:
                    args = dict(args or {})
                except Exception:
                    args = {}
            calls.append({"function": {"name": fn.get("name") or "", "arguments": args}})
        return calls

    @classmethod
    def _message(cls, raw: Dict[str, Any], content: Optional[str] = None) -> Dict[str, Any]:
        return {
            "role": "assistant",
            "content": (raw.get("content") or "") if content is None else content,
            "tool_calls": cls._normalize_calls(raw.get("tool_calls")),
        }

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
             temperature: Optional[float] = None, num_predict: Optional[int] = None) -> LLMReply:
        resp = self._request(messages, tools, temperature=temperature, num_predict=num_predict, stream=False)
        raw = _plain(_field(resp, "message")) or {}
        return LLMReply(self._message(raw), _field(resp, "prompt_eval_count"), _field(resp, "eval_count"))

    def chat_stream(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
                    on_token: TokenCallback, temperature: Optional[float] = None,
                    num_predict: Optional[int] = None, on_stats: Optional[Any] = None) -> LLMReply:
        """Stream content deltas through *on_token* and return the complete reply."""
        stream = self._request(messages, tools, temperature=temperature, num_predict=num_predict, stream=True)
        parts: List[str] = []
        calls: List[Dict[str, Any]] = []
        prompt_tokens = output_tokens = None
        try:
            for chunk in stream:
                raw = _plain(_field(chunk, "message")) or {}
                delta = raw.get("content") or ""
                if delta:
                    parts.append(delta)
                    on_token(delta)
                if raw.get("tool_calls"):
                    calls = self._normalize_calls(raw["tool_calls"])
                prompt = _field(chunk, "prompt_eval_count")
                if prompt is not None:
                    prompt_tokens = prompt
                output = _field(chunk, "eval_count")
                if output is not None:
                    output_tokens = output
        except Exception as exc:
            raise LLMError(f"Ollama stream failed: {exc}") from exc
        message = {"role": "assistant", "content": "".join(parts), "tool_calls": calls}
        return LLMReply(message, prompt_tokens, output_tokens)
