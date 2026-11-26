"""Serving-model chain for evals.

The default chain uses Google AI Studio's free models first and falls back to
the local Ollama model when a target is rate-limited (or temporarily
unavailable):

    gemma-4-31b-it -> gemma-4-26b-a4b-it -> gemini-3.5-flash-lite -> Ollama

Everything here is harness-owned. The application only sees the small
``chat`` / ``chat_stream`` interface that it already expects, so no application
code needs to know about Google AI Studio, fallback order, or rate limits.

Google AI Studio exposes an OpenAI-compatible endpoint, but it is stricter than
llama.cpp: tool calls need ids, arguments must be JSON strings, tool results
need a matching ``tool_call_id``, and Gemini 3 function calls need their
``thought_signature`` echoed back. ``ChatCompletionsLLM`` normalizes both
directions so the rest of the agent can keep its existing message shape.
"""

from __future__ import annotations

import copy
import json
import os
import re
import sys
import time
from dataclasses import dataclass, replace
from typing import Any, Dict, Iterable, List, Optional

import requests

from context_agent.config import Config
from context_agent.llm.errors import LLMError
from context_agent.llm.ollama import OllamaLLM
from context_agent.llm.reply import LLMReply
from context_agent.llm.streaming import TokenCallback

SERVING_PREFIX = "[eval-serving]"
FALLBACK_PREFIX = "[eval-fallback]"
RETRY_PREFIX = "[eval-retry]"

DEFAULT_GOOGLE_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
DEFAULT_GOOGLE_MODELS = (
    "gemma-4-31b-it",
    "gemma-4-26b-a4b-it",
    "gemini-3.5-flash-lite",
)
DEFAULT_GOOGLE_NUM_CTX = 16384
DEFAULT_OLLAMA_MODEL = "nemotron-3.5-bolt:e4b-64k"

GOOGLE_PROVIDERS = {"google", "gemini", "google-ai-studio", "google_ai_studio", "aistudio"}
LOCAL_PROVIDERS = {"local", "openai", "openai-compatible", "openai_compatible", "llama-cpp"}
FALLBACK_KINDS = {"rate_limit", "unavailable", "unsupported_tools", "invalid_model"}
# Kinds worth retrying on the same target before moving on. Google AI Studio
# answers 503 "overloaded" in bursts; with a single-target chain that used to
# abort the whole case.
RETRYABLE_KINDS = {"rate_limit", "unavailable"}

RATE_LIMIT_SIGNALS = (
    "429",
    "resource_exhausted",
    "resource exhausted",
    "rate limit",
    "rate-limit",
    "ratelimit",
    "too many requests",
    "quota",
    "tpm",
    "rpm",
    "requests per minute",
    "tokens per minute",
)
UNAVAILABLE_SIGNALS = (
    "503",
    "502",
    "504",
    "unavailable",
    "high demand",
    "overloaded",
    "try again later",
    "connection",
    "timed out",
    "timeout",
)
UNSUPPORTED_TOOL_SIGNALS = (
    "does not support tools",
    "does not support function",
    "function calling is not supported",
    "tools are not supported",
    "tool use is not supported",
)
INVALID_MODEL_SIGNALS = (
    "model not found",
    "is not found",
    "not found for api version",
    "not supported for generatecontent",
)
MISSING_PACKAGE_SIGNALS = (
    "no module named",
    "modulenotfounderror",
    "importerror",
    "pip install",
    "requires the `google.genai` package",
)

_THOUGHT_RE = re.compile(r"<(thought|thinking)>.*?</\1>", re.S | re.I)
_THOUGHT_CLOSE_RE = re.compile(r"</(?:thought|thinking)>", re.I)


def _log(message: str) -> None:
    """Print a harness log line even when pytest captures stdout."""
    # Write to the controlling terminal first so transient-error retries are
    # visible live instead of being swallowed by pytest's capture.
    try:
        with open("/dev/tty", "w", encoding="utf-8") as fh:
            print(message, file=fh, flush=True)
    except OSError:
        pass
    stream = getattr(sys, "__stdout__", None) or sys.stdout
    try:
        print(message, file=stream, flush=True)
    except Exception:  # pragma: no cover - a closed stream must not break a run
        pass


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off", ""}


def _env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


def google_api_key() -> Optional[str]:
    for name in (
        "EVAL_GOOGLE_API_KEY",
        "GOOGLE_AI_STUDIO_API_KEY",
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
    ):
        value = _env(name)
        if value:
            return value
    return None


def google_base_url() -> str:
    return _env("EVAL_GOOGLE_BASE_URL", DEFAULT_GOOGLE_BASE_URL).rstrip("/")


def google_models() -> List[str]:
    raw = _env("EVAL_GOOGLE_MODELS")
    if raw:
        models = [item.strip() for item in raw.split(",") if item.strip()]
    else:
        models = [
            _env("EVAL_GOOGLE_MODEL_PRIMARY", DEFAULT_GOOGLE_MODELS[0]),
            _env("EVAL_GOOGLE_MODEL_SECONDARY", DEFAULT_GOOGLE_MODELS[1]),
            _env("EVAL_GOOGLE_MODEL_TERTIARY", DEFAULT_GOOGLE_MODELS[2]),
        ]
    seen: set[str] = set()
    unique = []
    for model in models:
        if model not in seen:
            seen.add(model)
            unique.append(model)
    return unique


def serving_num_ctx() -> int:
    try:
        return int(_env("EVAL_SERVING_NUM_CTX", str(DEFAULT_GOOGLE_NUM_CTX)))
    except ValueError:
        return DEFAULT_GOOGLE_NUM_CTX


class ServingError(LLMError):
    """An LLM error carrying enough detail for the fallback chain to decide."""

    def __init__(self, message: str, *, status: Optional[int] = None,
                 kind: str = "error", detail: Optional[str] = None):
        super().__init__(message)
        self.status = status
        self.kind = kind
        self.detail = detail or message


def classify_error(status: Optional[int], text: str) -> str:
    """Classify an HTTP error as a fallback reason, or ``"fatal"``."""
    lower = (text or "").lower()
    if any(signal in lower for signal in MISSING_PACKAGE_SIGNALS):
        return "unavailable"
    if status == 429 or any(signal in lower for signal in RATE_LIMIT_SIGNALS):
        return "rate_limit"
    if status in {500, 502, 503, 504} or any(signal in lower for signal in UNAVAILABLE_SIGNALS):
        return "unavailable"
    if any(signal in lower for signal in UNSUPPORTED_TOOL_SIGNALS):
        return "unsupported_tools"
    if status == 404 or any(signal in lower for signal in INVALID_MODEL_SIGNALS):
        return "invalid_model"
    return "fatal"


def fallback_reason(exc: BaseException) -> Optional[str]:
    """Return the fallback reason for an exception, or ``None`` if fatal."""
    kind = getattr(exc, "kind", None)
    if kind in FALLBACK_KINDS:
        return kind
    if kind == "fatal":
        # The caller already classified this explicitly; do not re-guess from
        # the message text.
        return None
    text = str(exc or "")
    lower = text.lower()
    if any(signal in lower for signal in MISSING_PACKAGE_SIGNALS):
        return "unavailable"
    if any(signal in lower for signal in RATE_LIMIT_SIGNALS):
        return "rate_limit"
    if any(signal in lower for signal in UNAVAILABLE_SIGNALS):
        return "unavailable"
    if any(signal in lower for signal in UNSUPPORTED_TOOL_SIGNALS):
        return "unsupported_tools"
    if any(signal in lower for signal in INVALID_MODEL_SIGNALS):
        return "invalid_model"
    return None


def _clean_content(text: Any) -> str:
    value = text or ""
    if not isinstance(value, str):
        return value
    value = _THOUGHT_RE.sub("", value)
    if _THOUGHT_CLOSE_RE.search(value):
        value = _THOUGHT_CLOSE_RE.split(value)[-1]
    return value.strip()


def _canonical_args(args: Any) -> str:
    if isinstance(args, str):
        try:
            args = json.loads(args) if args.strip() else {}
        except json.JSONDecodeError:
            return args
    return json.dumps(args or {}, sort_keys=True, ensure_ascii=False, default=str)


def _parse_args(args: Any) -> Dict[str, Any]:
    if isinstance(args, str):
        try:
            args = json.loads(args) if args.strip() else {}
        except json.JSONDecodeError:
            args = {"__invalid_json__": args[:300]}
    if not isinstance(args, dict):
        try:
            args = dict(args or {})
        except Exception:
            args = {}
    return args


class ChatCompletionsLLM:
    """OpenAI-compatible client with Google AI Studio compatibility shims."""

    supports_streaming = True

    def __init__(self, cfg: Config, *, model: str, base_url: str, api_key: str,
                 label: str = "", require_tool_signatures: bool = False):
        self.cfg = cfg
        self.model = model
        self.label = label or model
        self.require_tool_signatures = require_tool_signatures
        self.base_url = (base_url or "").strip().rstrip("/")
        if not self.base_url:
            raise LLMError("an OpenAI-compatible base URL is required")
        self.chat_url = (
            self.base_url
            if self.base_url.endswith("/chat/completions")
            else f"{self.base_url}/chat/completions"
        )
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        # Google requires the thought signature from a function call to be
        # echoed back on the next turn. The application normalizes tool calls
        # down to name+arguments, so remember signatures under that key.
        self._signatures: Dict[tuple[str, str], Any] = {}
        self._ids: Dict[tuple[str, str], str] = {}
        self._next_id = 0
        # Set after Google rejects a replayed signature. From then on the
        # adapter replays tool exchanges as text, which is lossy but never
        # aborts an otherwise valid run.
        self._force_flatten = False

    # ---------------------------------------------------------------- outgoing
    def _remember_call(self, call: Dict[str, Any], name: str, args: Dict[str, Any],
                       call_id: Optional[str]) -> None:
        key = (name, _canonical_args(args))
        extra = call.get("extra_content")
        if extra:
            self._signatures[key] = extra
        if call_id:
            self._ids[key] = call_id

    def _new_id(self) -> str:
        self._next_id += 1
        return f"call_{self._next_id}"

    def _prepare_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert the agent's message shape into what Google's API accepts."""
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
                    raw_call = copy.deepcopy(raw_call or {})
                    fn = raw_call.get("function") or {}
                    name = fn.get("name") or ""
                    args = _parse_args(fn.get("arguments"))
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
                    if self._force_flatten and self.require_tool_signatures:
                        missing_signature = True
                    elif extra:
                        call["extra_content"] = copy.deepcopy(extra)
                    elif self.require_tool_signatures:
                        missing_signature = True
                        if _env_flag("EVAL_SERVING_DEBUG"):
                            _log(
                                f"[eval-serving-debug] no thought_signature for "
                                f"{self.label} {name}({_canonical_args(args)}); "
                                f"known keys={list(self._signatures)}"
                            )
                    calls.append(call)

                if missing_signature:
                    # Gemini rejects a function-call history without the
                    # original signature. Replaying it as plain text keeps the
                    # information (and the run) instead of aborting the case.
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

    # ---------------------------------------------------------------- request
    def _payload(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]],
                 stream: bool, temperature: Optional[float],
                 num_predict: Optional[int]) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": self._prepare_messages(messages),
            "temperature": self.cfg.temperature if temperature is None else temperature,
            "max_tokens": num_predict or self.cfg.num_predict,
            "stream": stream,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        return payload

    def _request(self, payload: Dict[str, Any], stream: bool) -> requests.Response:
        try:
            response = self._session.post(
                self.chat_url,
                json=payload,
                timeout=self.cfg.request_timeout,
                stream=stream,
            )
        except requests.RequestException as exc:
            raise ServingError(
                f"{self.label} endpoint unavailable at {self.chat_url}: {exc}",
                kind="unavailable",
                detail=str(exc),
            ) from exc

        if response.status_code >= 400:
            detail = ""
            try:
                detail = response.text[:800]
            except Exception:
                pass
            kind = classify_error(response.status_code, detail)
            raise ServingError(
                f"{self.label} request failed (HTTP {response.status_code}): {detail[:300]}",
                status=response.status_code,
                kind=kind,
                detail=detail,
            )
        return response

    def _retry_without_signatures(self, exc: ServingError) -> bool:
        if self._force_flatten or not self.require_tool_signatures:
            return False
        detail = (getattr(exc, "detail", "") or str(exc)).lower()
        if getattr(exc, "status", None) != 400:
            return False
        if "thought_signature" not in detail and "thought signature" not in detail:
            return False
        self._force_flatten = True
        _log(
            f"{SERVING_PREFIX} {self.label} rejected a tool thought_signature; "
            "replaying prior tool exchanges as text"
        )
        return True

    # ---------------------------------------------------------------- replies
    def _normalize_calls(self, raw_calls: Any) -> List[Dict[str, Any]]:
        calls: List[Dict[str, Any]] = []
        for raw in raw_calls or []:
            raw = raw or {}
            fn = raw.get("function") or {}
            name = fn.get("name") or ""
            args = _parse_args(fn.get("arguments"))
            call_id = raw.get("id")
            self._remember_call(raw, name, args, call_id)
            if _env_flag("EVAL_SERVING_DEBUG"):
                _log(
                    f"[eval-serving-debug] {self.label} tool call "
                    f"{name}({_canonical_args(args)}) id={call_id} "
                    f"signature={'yes' if raw.get('extra_content') else 'no'}"
                )
            call: Dict[str, Any] = {
                "function": {"name": name, "arguments": args},
            }
            if call_id:
                call["id"] = call_id
            if raw.get("extra_content"):
                call["extra_content"] = copy.deepcopy(raw["extra_content"])
            calls.append(call)
        return calls

    def _reply(self, data: Dict[str, Any]) -> LLMReply:
        choice = (data.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        usage = data.get("usage") or {}
        return LLMReply(
            {
                "role": message.get("role") or "assistant",
                "content": _clean_content(message.get("content")),
                "tool_calls": self._normalize_calls(message.get("tool_calls")),
            },
            usage.get("prompt_tokens"),
            usage.get("completion_tokens"),
        )

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
             temperature: Optional[float] = None,
             num_predict: Optional[int] = None) -> LLMReply:
        payload = self._payload(messages, tools, False, temperature, num_predict)
        try:
            response = self._request(payload, False)
        except ServingError as exc:
            if not self._retry_without_signatures(exc):
                raise
            payload = self._payload(messages, tools, False, temperature, num_predict)
            response = self._request(payload, False)
        try:
            data = response.json()
        except Exception as exc:
            raise ServingError(f"{self.label} returned invalid JSON") from exc
        return self._reply(data)

    # ---------------------------------------------------------------- streaming
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

    def chat_stream(self, messages: List[Dict[str, Any]],
                    tools: Optional[List[Dict[str, Any]]] = None, *,
                    on_token: TokenCallback,
                    temperature: Optional[float] = None,
                    num_predict: Optional[int] = None) -> LLMReply:
        payload = self._payload(messages, tools, True, temperature, num_predict)
        try:
            response = self._request(payload, True)
        except ServingError as exc:
            if not self._retry_without_signatures(exc):
                raise
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
                    raise ServingError(
                        f"{self.label} returned invalid streaming JSON: {line[:200]}",
                        kind="fatal",
                    ) from exc
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
                    current = call_parts.setdefault(
                        index,
                        {"id": "", "extra_content": None,
                         "function": {"name": "", "arguments": ""}},
                    )
                    if call.get("id"):
                        current["id"] = call["id"]
                    if call.get("extra_content"):
                        current["extra_content"] = call["extra_content"]
                    function = call.get("function") or {}
                    if function.get("name"):
                        current["function"]["name"] += function["name"]
                    if function.get("arguments"):
                        current["function"]["arguments"] += function["arguments"]
        except requests.RequestException as exc:
            raise ServingError(
                f"{self.label} stream failed at {self.chat_url}: {exc}",
                kind="unavailable",
                detail=str(exc),
            ) from exc

        calls = []
        for index in sorted(call_parts):
            call = call_parts[index]
            args_text = call["function"]["arguments"]
            try:
                args = json.loads(args_text) if args_text.strip() else {}
            except json.JSONDecodeError:
                args = {"__invalid_json__": args_text[:300]}
            raw = {
                "id": call.get("id") or self._new_id(),
                "function": {"name": call["function"]["name"], "arguments": args},
            }
            if call.get("extra_content"):
                raw["extra_content"] = call["extra_content"]
            calls.append(raw)

        message = {
            "role": "assistant",
            "content": _clean_content("".join(parts)),
            "tool_calls": self._normalize_calls(calls),
        }
        return LLMReply(message, prompt_tokens, output_tokens)


@dataclass
class ServingTarget:
    label: str
    provider: str
    model: str
    llm: Any

    @property
    def display(self) -> str:
        return self.label


class FallbackLLM:
    """Try targets in order, switching only on retryable failures.

    Fallback is sticky for the rest of the process: once a target has been
    rate-limited there is no point retrying it on every step of the same run.
    """

    supports_streaming = True

    def __init__(self, targets: List[ServingTarget], *, num_ctx: int = DEFAULT_GOOGLE_NUM_CTX):
        if not targets:
            raise ValueError("FallbackLLM needs at least one target")
        self.targets = list(targets)
        self.index = 0
        self.switches: List[Dict[str, str]] = []
        self.retries: List[Dict[str, str]] = []
        self.num_ctx = num_ctx
        self._announced = False
        _log(f"{SERVING_PREFIX} chain: " + " -> ".join(target.label for target in self.targets))

    @property
    def active(self) -> ServingTarget:
        return self.targets[self.index]

    @property
    def active_label(self) -> str:
        return self.active.label

    # Rolling backoff for transient 503/429 bursts: short waits first, capped at
    # 10s. Replaces the old flat 2s-doubling schedule so a one-off blip clears
    # quickly while a sustained spike still gets a real chance to recover.
    _RETRY_DELAYS = (3.0, 5.0, 7.0, 10.0)

    @property
    def max_retries(self) -> int:
        try:
            return max(0, int(_env("EVAL_SERVING_RETRIES", "4")))
        except ValueError:
            return 4

    def _retry_delay(self, attempt: int) -> float:
        if attempt < len(self._RETRY_DELAYS):
            return self._RETRY_DELAYS[attempt]
        return self._RETRY_DELAYS[-1]

    def _announce(self) -> None:
        if not self._announced:
            self._announced = True
            _log(f"{SERVING_PREFIX} using {self.active.label}")

    def _can_fallback(self, exc: BaseException) -> Optional[str]:
        if self.index >= len(self.targets) - 1:
            return None
        return fallback_reason(exc)

    def _should_retry_same(self, exc: BaseException, attempt: int) -> bool:
        """Whether to retry the current target instead of advancing.

        Transient overloads (503/502/timeout) are retried on the same target
        first. Rate limits skip ahead to the next target when there is one,
        because the quota is per-model; on the last target they get a backoff
        retry too.
        """
        if attempt >= self.max_retries:
            return False
        kind = fallback_reason(exc)
        if kind not in RETRYABLE_KINDS:
            return False
        if kind == "rate_limit" and self.index < len(self.targets) - 1:
            return False
        return True

    def _pause_before_retry(self, exc: BaseException, attempt: int) -> None:
        reason = fallback_reason(exc) or "unavailable"
        delay = self._retry_delay(attempt)
        detail = " ".join(str(exc or "").split())[:200]
        _log(
            f"{RETRY_PREFIX} {reason} on {self.active.label}: {detail} "
            f"-> retry {attempt + 1}/{self.max_retries} in {delay:.0f}s"
        )
        self.retries.append({
            "target": self.active.label,
            "reason": reason,
            "detail": detail,
            "delay": f"{delay:.0f}",
        })
        if delay > 0:
            time.sleep(delay)

    def _advance(self, reason: str, exc: BaseException) -> None:
        previous = self.active
        self.index += 1
        following = self.active
        detail = " ".join(str(exc or "").split())[:240]
        self.switches.append({
            "from": previous.label,
            "to": following.label,
            "reason": reason,
            "detail": detail,
        })
        _log(
            f"{FALLBACK_PREFIX} {reason} on {previous.label}: {detail} "
            f"-> switching to {following.label}"
        )

    def chat(self, messages: List[Dict[str, Any]],
             tools: Optional[List[Dict[str, Any]]] = None, *,
             temperature: Optional[float] = None,
             num_predict: Optional[int] = None) -> LLMReply:
        self._announce()
        attempt = 0
        while True:
            target = self.active
            try:
                return target.llm.chat(
                    messages, tools, temperature=temperature, num_predict=num_predict
                )
            except Exception as exc:
                if self._should_retry_same(exc, attempt):
                    self._pause_before_retry(exc, attempt)
                    attempt += 1
                    continue
                reason = self._can_fallback(exc)
                if reason is None:
                    raise
                self._advance(reason, exc)
                attempt = 0

    def chat_stream(self, messages: List[Dict[str, Any]],
                    tools: Optional[List[Dict[str, Any]]] = None, *,
                    on_token: TokenCallback,
                    temperature: Optional[float] = None,
                    num_predict: Optional[int] = None) -> LLMReply:
        self._announce()
        attempt = 0
        while True:
            target = self.active
            emitted = False

            def wrapped(token: str) -> None:
                nonlocal emitted
                emitted = True
                on_token(token)

            try:
                return target.llm.chat_stream(
                    messages, tools, on_token=wrapped,
                    temperature=temperature, num_predict=num_predict,
                )
            except Exception as exc:
                # Never replay a partially streamed answer: that would duplicate
                # text and corrupt the conversation.
                if emitted:
                    raise
                if self._should_retry_same(exc, attempt):
                    self._pause_before_retry(exc, attempt)
                    attempt += 1
                    continue
                reason = self._can_fallback(exc)
                if reason is None:
                    raise
                self._advance(reason, exc)
                attempt = 0


# --------------------------------------------------------------------- planning
def _chain_specs() -> List[tuple[str, str]]:
    raw = _env("EVAL_SERVING_CHAIN")
    if raw:
        specs: List[tuple[str, str]] = []
        for item in raw.split(","):
            item = item.strip()
            if not item:
                continue
            provider, separator, model = item.partition(":")
            if separator and provider.strip().lower() in GOOGLE_PROVIDERS | LOCAL_PROVIDERS | {"ollama"}:
                specs.append((provider.strip().lower(), model.strip()))
            else:
                specs.append(("", item))
        return specs

    specs = []
    key = google_api_key()
    if key:
        specs.extend(("google", model) for model in google_models())
    specs.append((
        "ollama",
        _env("EVAL_OLLAMA_FALLBACK_MODEL", _env("AGENT_MODEL", DEFAULT_OLLAMA_MODEL)),
    ))
    return specs


def _normalize_provider(provider: str) -> str:
    value = (provider or "").strip().lower()
    if value in GOOGLE_PROVIDERS:
        return "google"
    if value in LOCAL_PROVIDERS:
        return "local"
    if value == "ollama":
        return "ollama"
    return value


def _spec_label(provider: str, model: str) -> str:
    provider = _normalize_provider(provider)
    return f"{provider or 'model'}/{model}"


def describe_chain() -> Optional[str]:
    """Return a human-readable chain without constructing clients, or ``None``."""
    if _env_flag("EVAL_SERVING_DISABLE"):
        return None
    explicit_provider = _normalize_provider(_env("AGENT_PROVIDER"))
    chain = _env("EVAL_SERVING_CHAIN")
    key = google_api_key()
    if not chain and explicit_provider and explicit_provider != "google":
        return None
    if not chain and not key:
        return None
    specs = _chain_specs()
    labels = []
    for provider, model in specs:
        if not provider:
            provider = "google" if key else "ollama"
        labels.append(_spec_label(provider, model))
    if _env_flag("EVAL_SERVING_FINAL_OLLAMA", True) and labels and not labels[-1].startswith("ollama/"):
        labels.append(_spec_label(
            "ollama",
            _env("EVAL_OLLAMA_FALLBACK_MODEL", _env("AGENT_MODEL", DEFAULT_OLLAMA_MODEL)),
        ))
    return " -> ".join(labels) if labels else None


def _ollama_target(cfg: Config) -> ServingTarget:
    model = _env("EVAL_OLLAMA_FALLBACK_MODEL", cfg.model or DEFAULT_OLLAMA_MODEL)
    try:
        num_ctx = int(_env("EVAL_OLLAMA_FALLBACK_NUM_CTX", str(serving_num_ctx())))
    except ValueError:
        num_ctx = serving_num_ctx()
    ollama_cfg = replace(
        cfg,
        provider="ollama",
        model=model,
        num_ctx=num_ctx,
    )
    return ServingTarget(
        label=_spec_label("ollama", model),
        provider="ollama",
        model=model,
        llm=OllamaLLM(ollama_cfg),
    )


def _local_target(cfg: Config, model: str) -> ServingTarget:
    base_url = (
        _env("EVAL_SERVING_BASE_URL")
        or _env("AGENT_BASE_URL")
        or _env("LLAMA_CPP_BASE_URL")
    )
    api_key = (
        _env("EVAL_SERVING_API_KEY")
        or _env("AGENT_API_KEY")
        or _env("LLAMA_CPP_API_KEY")
        or "local"
    )
    if not base_url:
        raise LLMError(
            "EVAL_SERVING_CHAIN uses a local target but no base URL is set; "
            "use EVAL_SERVING_BASE_URL or AGENT_BASE_URL"
        )
    local_cfg = replace(cfg, provider="local", model=model, base_url=base_url, api_key=api_key)
    return ServingTarget(
        label=_spec_label("local", model),
        provider="local",
        model=model,
        llm=ChatCompletionsLLM(
            local_cfg, model=model, base_url=base_url, api_key=api_key,
            label=_spec_label("local", model),
        ),
    )


def build_serving_targets(cfg: Config) -> List[ServingTarget]:
    key = google_api_key()
    base_url = google_base_url()
    specs = _chain_specs()
    targets: List[ServingTarget] = []
    for provider, model in specs:
        provider = _normalize_provider(provider)
        if not provider:
            provider = "google" if key else "ollama"
        if provider == "google":
            if not key:
                raise LLMError(
                    "Google AI Studio is in the eval serving chain but no API key is set. "
                    "Set GEMINI_API_KEY (or GOOGLE_API_KEY), or remove Google targets "
                    "from EVAL_SERVING_CHAIN."
                )
            google_cfg = replace(cfg, provider="google", model=model,
                                 base_url=base_url, api_key=key)
            targets.append(ServingTarget(
                label=_spec_label("google", model),
                provider="google",
                model=model,
                llm=ChatCompletionsLLM(
                    google_cfg, model=model, base_url=base_url, api_key=key,
                    label=_spec_label("google", model),
                    require_tool_signatures=True,
                ),
            ))
        elif provider == "ollama":
            targets.append(_ollama_target(cfg))
        elif provider == "local":
            targets.append(_local_target(cfg, model))
        else:
            raise LLMError(f"unknown serving provider {provider!r} in EVAL_SERVING_CHAIN")

    if _env_flag("EVAL_SERVING_FINAL_OLLAMA", True) and targets:
        if targets[-1].provider != "ollama":
            targets.append(_ollama_target(cfg))
    return targets


def build_serving_llm(cfg: Config) -> Optional[FallbackLLM]:
    """Build the configured fallback chain, or ``None`` to use the app default."""
    if _env_flag("EVAL_SERVING_DISABLE"):
        return None

    explicit_provider = _normalize_provider(_env("AGENT_PROVIDER"))
    chain = _env("EVAL_SERVING_CHAIN")
    key = google_api_key()

    if not chain:
        # An explicit non-Google provider means "use the app's own adapter".
        if explicit_provider and explicit_provider != "google":
            return None
        if not key:
            if explicit_provider == "google":
                raise LLMError(
                    "AGENT_PROVIDER=google requires GEMINI_API_KEY or GOOGLE_API_KEY"
                )
            return None

    targets = build_serving_targets(cfg)
    if not targets:
        return None
    return FallbackLLM(targets, num_ctx=serving_num_ctx())


__all__ = [
    "ChatCompletionsLLM",
    "FallbackLLM",
    "ServingError",
    "ServingTarget",
    "build_serving_llm",
    "build_serving_targets",
    "classify_error",
    "describe_chain",
    "fallback_reason",
    "google_api_key",
    "google_models",
    "serving_num_ctx",
]
