"""OpenAI-compatible adapter for llama.cpp server and llama.cpp macOS app."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Iterable, List, Optional

import requests

from ..config import Config
from .errors import LLMError
from .reply import LLMReply
from .streaming import TokenCallback


class LlamaCppLLM:
    supports_streaming = True

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.base_url = self._normalize_base_url(cfg.base_url or "http://127.0.0.1:8080/v1")
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        if cfg.api_key:
            self._session.headers["Authorization"] = f"Bearer {cfg.api_key}"

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        url = (base_url or "").strip().rstrip("/")
        if not url:
            url = "http://127.0.0.1:8080/v1"
        if url.endswith("/chat/completions"):
            return url[:-len("/chat/completions")]
        if not url.endswith("/v1"):
            url = f"{url}/v1"
        return url

    @property
    def chat_url(self) -> str:
        return f"{self.base_url}/chat/completions"

    def _payload(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]],
                 stream: bool, temperature: Optional[float], num_predict: Optional[int]) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.cfg.model,
            "messages": messages,
            "temperature": self.cfg.temperature if temperature is None else temperature,
            "max_tokens": num_predict or self.cfg.num_predict,
            "stream": stream,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        return payload

    @staticmethod
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

    @staticmethod
    def _normalize_calls(raw_calls: Any) -> List[Dict[str, Any]]:
        calls = []
        for call in LlamaCppLLM._plain(raw_calls) or []:
            call = LlamaCppLLM._plain(call) or {}
            fn = LlamaCppLLM._plain(call.get("function")) or {}
            args = fn.get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args) if args.strip() else {}
                except json.JSONDecodeError:
                    args = {"__invalid_json__": args[:300]}
            if not isinstance(args, dict):
                args = {}
            calls.append({"function": {"name": fn.get("name") or "", "arguments": args}})
        return calls

    def _request(self, payload: Dict[str, Any], stream: bool) -> requests.Response:
        for attempt in range(2):
            try:
                response = self._session.post(
                    self.chat_url,
                    json=payload,
                    timeout=self.cfg.request_timeout,
                    stream=stream,
                )
                if response.status_code >= 400:
                    detail = ""
                    try:
                        detail = response.text[:500]
                    except Exception:
                        pass
                    raise LLMError(
                        f"llama.cpp request failed ({response.status_code}) at {self.chat_url}: {detail}"
                    )
                return response
            except LLMError:
                raise
            except requests.RequestException as exc:
                if attempt == 0:
                    time.sleep(1.0)
                    continue
                raise LLMError(f"llama.cpp endpoint unavailable at {self.chat_url}: {exc}") from exc
        raise LLMError(f"llama.cpp endpoint unavailable at {self.chat_url}")

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
             temperature: Optional[float] = None, num_predict: Optional[int] = None) -> LLMReply:
        payload = self._payload(messages, tools, False, temperature, num_predict)
        response = self._request(payload, False)
        try:
            data = response.json()
        except Exception as exc:
            raise LLMError(f"llama.cpp returned invalid JSON from {self.chat_url}") from exc
        choice = (data.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        usage = data.get("usage") or {}
        return LLMReply(
            {
                "role": message.get("role") or "assistant",
                "content": message.get("content") or "",
                "tool_calls": self._normalize_calls(message.get("tool_calls")),
            },
            usage.get("prompt_tokens"),
            usage.get("completion_tokens"),
        )

    @staticmethod
    def _stream_lines(response: requests.Response) -> Iterable[str]:
        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            if isinstance(raw_line, bytes):
                raw_line = raw_line.decode("utf-8", "replace")
            line = raw_line.strip()
            if line.startswith("data:"):
                line = line[len("data:"):].strip()
            if line:
                yield line

    def chat_stream(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
                    on_token: TokenCallback, temperature: Optional[float] = None,
                    num_predict: Optional[int] = None, on_stats: Optional[Any] = None) -> LLMReply:
        payload = self._payload(messages, tools, True, temperature, num_predict)
        response = self._request(payload, True)
        parts: List[str] = []
        call_parts: Dict[int, Dict[str, Any]] = {}
        prompt_tokens = output_tokens = None

        try:
            for line in self._stream_lines(response):
                if line == "[DONE]":
                    break
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise LLMError(f"llama.cpp returned invalid streaming JSON: {line[:200]}") from exc
                usage = chunk.get("usage") or {}
                if usage:
                    prompt_tokens = usage.get("prompt_tokens") or prompt_tokens
                    output_tokens = usage.get("completion_tokens") or output_tokens
                choice = (chunk.get("choices") or [{}])[0]
                delta = choice.get("delta") or {}
                content = delta.get("content")
                if content:
                    parts.append(content)
                    on_token(content)
                for call in delta.get("tool_calls") or []:
                    index = int(call.get("index", 0))
                    current = call_parts.setdefault(index, {"id": "", "function": {"name": "", "arguments": ""}})
                    if call.get("id"):
                        current["id"] = call["id"]
                    function = call.get("function") or {}
                    if function.get("name"):
                        current["function"]["name"] += function["name"]
                    if function.get("arguments"):
                        current["function"]["arguments"] += function["arguments"]
        except requests.RequestException as exc:
            raise LLMError(f"llama.cpp stream failed at {self.chat_url}: {exc}") from exc

        calls = []
        for index in sorted(call_parts):
            call = call_parts[index]
            args_text = call["function"]["arguments"]
            try:
                args = json.loads(args_text) if args_text.strip() else {}
            except json.JSONDecodeError:
                args = {"__invalid_json__": args_text[:300]}
            calls.append({"function": {"name": call["function"]["name"], "arguments": args}})
        return LLMReply(
            {"role": "assistant", "content": "".join(parts), "tool_calls": calls},
            prompt_tokens,
            output_tokens,
        )
