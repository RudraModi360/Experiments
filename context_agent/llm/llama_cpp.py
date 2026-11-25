"""OpenAI-compatible adapter for llama.cpp and Google AI Studio.

The same wire protocol covers llama.cpp's server, the llama.cpp macOS app and
Google AI Studio's OpenAI-compatible endpoint. Gemini is stricter: tool calls
need ids, tool results need a matching ``tool_call_id`` and Gemini 3 function
calls need their ``thought_signature`` echoed back on the next turn. When the
endpoint is Google (or ``google=True``), the adapter adds that bookkeeping and
never sends an invalid history.
"""

from __future__ import annotations

import copy
import json
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

from ..config import Config
from .errors import LLMError
from .reply import LLMReply
from .streaming import TokenCallback


def _canonical_args(args: Any) -> str:
    if isinstance(args, str):
        return args
    try:
        return json.dumps(args or {}, sort_keys=True, separators=(",", ":"), default=str)
    except (TypeError, ValueError):
        return str(args)


class LlamaCppLLM:
    supports_streaming = True

    def __init__(self, cfg: Config, *, google: bool = False):
        self.cfg = cfg
        self.base_url = self._normalize_base_url(cfg.base_url or "http://127.0.0.1:8080/v1")
        self._google = bool(google or "generativelanguage.googleapis.com" in self.base_url)
        # Gemini needs signatures/ids from the previous reply. Keep them under
        # (name, canonical args) because the agent stores calls without extras.
        self._signatures: Dict[Tuple[str, str], Any] = {}
        self._ids: Dict[Tuple[str, str], str] = {}
        self._next_id = 0
        self._force_flatten = False
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
        # Google AI Studio's compatible base is .../v1beta/openai, not .../v1.
        if "generativelanguage.googleapis.com" in url:
            return url
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
            "messages": self._messages(messages) if self._google else messages,
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

    def _remember_call(self, name: str, args: Dict[str, Any], call_id: Optional[str],
                       extra: Any) -> None:
        key = (name, _canonical_args(args))
        if extra:
            self._signatures[key] = extra
        if call_id:
            self._ids[key] = call_id

    def _new_id(self) -> str:
        self._next_id += 1
        return f"call_{self._next_id}"

    def _messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert the agent's history into what Google's endpoint accepts."""
        prepared: List[Dict[str, Any]] = []
        pending_ids: List[str] = []
        flatten_tools = False

        for original in messages:
            message = copy.deepcopy(original or {})
            role = message.get("role")
            message.pop("_meta", None)
            if role != "tool":
                flatten_tools = False

            if role == "assistant" and message.get("tool_calls"):
                calls = []
                missing_signature = False
                pending_ids = []
                for raw_call in message.get("tool_calls") or []:
                    raw_call = self._plain(raw_call) or {}
                    fn = self._plain(raw_call.get("function")) or {}
                    name = fn.get("name") or ""
                    args = self._plain(fn.get("arguments"))
                    if isinstance(args, str):
                        try:
                            args = json.loads(args) if args.strip() else {}
                        except json.JSONDecodeError:
                            args = {"__invalid_json__": args[:300]}
                    if not isinstance(args, dict):
                        args = {}
                    key = (name, _canonical_args(args))
                    call_id = raw_call.get("id") or self._ids.get(key) or self._new_id()
                    pending_ids.append(call_id)
                    call = {
                        "id": call_id,
                        "type": "function",
                        "function": {
                            "name": name,
                            "arguments": _canonical_args(args),
                        },
                    }
                    extra = raw_call.get("extra_content") or self._signatures.get(key)
                    if self._force_flatten:
                        missing_signature = True
                    elif extra:
                        call["extra_content"] = copy.deepcopy(extra)
                    else:
                        missing_signature = True
                    calls.append(call)

                if missing_signature:
                    # Gemini rejects a function-call history without its
                    # original signature. Replay it as text so a resumed or
                    # compacted session keeps working instead of erroring out.
                    text = message.get("content") or ""
                    summary = "\n".join(
                        f"{call['function']['name']}({call['function']['arguments']})"
                        for call in calls
                    )
                    message.pop("tool_calls", None)
                    message["role"] = "assistant"
                    message["content"] = (
                        (text + "\n" if text else "")
                        + "[Previous tool calls - replayed without signatures]\n"
                        + summary
                    ).strip()
                    flatten_tools = True
                    pending_ids = []
                else:
                    message["tool_calls"] = calls
                    if message.get("content") is None:
                        message["content"] = ""

            elif role == "tool":
                if flatten_tools:
                    name = message.get("tool_name") or "tool"
                    content = message.get("content") or ""
                    prepared.append({
                        "role": "user",
                        "content": f"[Tool result: {name}]\n{content}",
                    })
                    continue
                call_id = message.get("tool_call_id")
                if not call_id and pending_ids:
                    call_id = pending_ids.pop(0)
                if not call_id:
                    call_id = self._new_id()
                message["tool_call_id"] = call_id
                message.pop("tool_name", None)
                if message.get("content") is None:
                    message["content"] = ""

            elif role == "assistant" and message.get("content") is None:
                message["content"] = ""

            prepared.append(message)
        return prepared

    def _normalize_calls(self, raw_calls: Any) -> List[Dict[str, Any]]:
        calls = []
        for call in self._plain(raw_calls) or []:
            call = self._plain(call) or {}
            fn = self._plain(call.get("function")) or {}
            args = fn.get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args) if args.strip() else {}
                except json.JSONDecodeError:
                    args = {"__invalid_json__": args[:300]}
            if not isinstance(args, dict):
                args = {}
            name = fn.get("name") or ""
            call_id = call.get("id") or None
            extra = call.get("extra_content")
            if self._google:
                self._remember_call(name, args, call_id, extra)
            normalized: Dict[str, Any] = {"function": {"name": name, "arguments": args}}
            if self._google:
                if call_id:
                    normalized["id"] = call_id
                if extra:
                    normalized["extra_content"] = copy.deepcopy(extra)
            calls.append(normalized)
        return calls

    _RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
    _RETRY_DELAYS = (3.0, 5.0, 7.0, 10.0)  # rolling backoff, capped at 10s
    _MAX_RETRIES = 10

    def _retry_delay(self, attempt: int) -> float:
        if attempt < len(self._RETRY_DELAYS):
            return self._RETRY_DELAYS[attempt]
        return self._RETRY_DELAYS[-1]

    def _request(self, payload: Dict[str, Any], stream: bool) -> requests.Response:
        last_exc: Optional[LLMError] = None
        for attempt in range(self._MAX_RETRIES + 1):
            try:
                response = self._session.post(
                    self.chat_url,
                    json=payload,
                    timeout=self.cfg.request_timeout,
                    stream=stream,
                )
            except requests.RequestException as exc:
                last_exc = LLMError(
                    f"llama.cpp endpoint unavailable at {self.chat_url}: {exc}"
                )
                if attempt < self._MAX_RETRIES:
                    delay = self._retry_delay(attempt)
                    print(
                        f"[llm] network error ({exc}); "
                        f"retry {attempt + 1}/{self._MAX_RETRIES} in {delay:.0f}s",
                        flush=True,
                    )
                    time.sleep(delay)
                    continue
                raise last_exc

            if response.status_code in self._RETRYABLE_STATUSES:
                detail = ""
                try:
                    detail = response.text[:500]
                except Exception:
                    pass
                last_exc = LLMError(
                    f"llama.cpp request failed ({response.status_code}) at {self.chat_url}: {detail}"
                )
                if attempt < self._MAX_RETRIES:
                    delay = self._retry_delay(attempt)
                    print(
                        f"[llm] HTTP {response.status_code} (transient); "
                        f"retry {attempt + 1}/{self._MAX_RETRIES} in {delay:.0f}s",
                        flush=True,
                    )
                    time.sleep(delay)
                    continue
                raise last_exc

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

        raise last_exc or LLMError(f"llama.cpp request failed at {self.chat_url}")

    @staticmethod
    def _is_signature_error(exc: BaseException) -> bool:
        text = str(exc or "").lower()
        return "400" in text and (
            "thought_signature" in text or "thought signature" in text
        )

    def _send(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]],
              stream: bool, temperature: Optional[float],
              num_predict: Optional[int]) -> requests.Response:
        payload = self._payload(messages, tools, stream, temperature, num_predict)
        try:
            return self._request(payload, stream)
        except LLMError as exc:
            if self._google and not self._force_flatten and self._is_signature_error(exc):
                # Google rejected a replayed signature: fall back to text
                # tool history instead of failing the turn.
                self._force_flatten = True
                payload = self._payload(messages, tools, stream, temperature, num_predict)
                return self._request(payload, stream)
            raise

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
             temperature: Optional[float] = None, num_predict: Optional[int] = None) -> LLMReply:
        response = self._send(messages, tools, False, temperature, num_predict)
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
        response = self._send(messages, tools, True, temperature, num_predict)
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
