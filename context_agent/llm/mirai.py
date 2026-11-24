"""Mirai/Uzu chat adapter for the trymirai Qwen model.

Uzu owns the model runtime; the agent keeps owning the conversation and tool
execution. Two details matter for this split:

* Tools must be registered on the ``ChatSession`` (message-level ``tools``
  blocks are rejected by the Mirai backend). ``tool_turn_limit=0`` makes uzu
  advertise them without executing them, so calls come back in the reply and
  the agent's own tool registry runs them.
* ``ChatSession.reply`` appends to the session's history. The agent already
  rebuilds the full history every step, so the session is reset before each
  reply to avoid duplicating turns.
"""

from __future__ import annotations

import asyncio
import json
import threading
from typing import Any, Dict, List, Optional

from ..config import Config
from .errors import LLMError
from .reply import LLMReply
from .streaming import TokenCallback

_SCHEMA_TOOL_CLASS: Any = None


def _schema_tool_class() -> Any:
    """Build (once) a UzuToolFunction wrapper that only advertises a schema."""
    global _SCHEMA_TOOL_CLASS
    if _SCHEMA_TOOL_CLASS is None:
        import uzu

        class _SchemaTool(uzu.UzuToolFunction):
            def __init__(self, tool_function: Any) -> None:
                self._tool_function = tool_function
                self.name = tool_function.name
                self.description = tool_function.description

            def _native_definition(self) -> Any:
                return self._tool_function

            def __call__(self, *args: Any, **kwargs: Any) -> str:
                # Never invoked: tool_turn_limit(0) disables uzu execution.
                return ""

        _SCHEMA_TOOL_CLASS = _SchemaTool
    return _SCHEMA_TOOL_CLASS


class MiraiLLM:
    supports_streaming = True

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._engine = None
        self._model = None
        self._session = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._ready = threading.Event()
        self._ready_error: Optional[BaseException] = None
        self._start()

    def _start(self) -> None:
        self._thread = threading.Thread(target=self._run_loop, name="mirai-uzu", daemon=True)
        self._thread.start()
        if not self._ready.wait(timeout=self.cfg.request_timeout):
            raise LLMError("Timed out while starting the Mirai/Uzu engine")
        if self._ready_error is not None:
            raise LLMError(f"Mirai/Uzu startup failed: {self._ready_error}")

    def _run_loop(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop
        try:
            loop.run_until_complete(self._initialize())
        except BaseException as exc:
            self._ready_error = exc
            self._ready.set()
        else:
            self._ready.set()
            loop.run_forever()
        finally:
            loop.close()

    async def _initialize(self) -> None:
        try:
            import uzu
        except ImportError as exc:
            raise LLMError("The 'uzu' python package is missing. Install the project dependencies: uv sync") from exc

        engine_config = uzu.EngineConfig.create()
        self._engine = await uzu.Engine.create(engine_config)
        self._model = await self._engine.model(self.cfg.model)
        if self._model is None:
            raise LLMError(f"Mirai model not found: {self.cfg.model}")

        async for _update in (await self._engine.download(self._model)).iterator():
            pass

        self._chat_config = uzu.ChatConfig.create().with_context_length(
            uzu.ContextLength.Custom(self.cfg.num_ctx)
        )
        self._session = await self._engine.chat(self._model, self._chat_config)

    async def _new_session(self) -> None:
        """Replace a stuck session. Heavy model weights stay loaded in the engine."""
        if self._engine is None or self._model is None:
            raise LLMError("Mirai/Uzu engine is not ready")
        self._session = await self._engine.chat(self._model, self._chat_config)

    def _run(self, awaitable: Any) -> Any:
        if self._loop is None:
            raise LLMError("Mirai/Uzu engine is not running")
        future = asyncio.run_coroutine_threadsafe(awaitable, self._loop)
        try:
            return future.result(timeout=self.cfg.request_timeout)
        except asyncio.TimeoutError as exc:
            future.cancel()
            raise LLMError("Mirai/Uzu request timed out") from exc
        except KeyboardInterrupt:
            # Ctrl-C interrupts this wait, but the coroutine keeps generating
            # on the engine thread and leaves the session in Generation state.
            future.cancel()
            raise
        except Exception as exc:
            if isinstance(exc, LLMError):
                raise
            raise LLMError(f"Mirai/Uzu call failed: {exc}") from exc

    async def _prepare(self, tools: Optional[List[Dict[str, Any]]]) -> None:
        """Start a clean session and register the agent's tools for this turn."""
        import uzu

        if self._session is None:
            raise LLMError("Mirai/Uzu session is not ready")
        # A cancelled generation (Ctrl-C) leaves the session in Generation state
        # where reset() itself fails. Recreate it instead of trying to reset.
        state = await self._session.state()
        if state != uzu.ChatSessionState.Idle:
            await self._new_session()
        else:
            # The agent replays the full history each step; uzu would otherwise
            # append it to its own history and duplicate every turn.
            await self._session.reset()
        if not tools:
            return

        wrappers = []
        schema_tool = _schema_tool_class()
        for tool in tools:
            function = tool.get("function") or {}
            name = function.get("name") or ""
            if not name:
                continue
            tool_function = uzu.ToolFunction(
                name,
                function.get("description") or "",
                uzu.Value(json.dumps(function.get("parameters") or {
                    "type": "object",
                    "properties": {},
                    "required": [],
                })),
                None,
            )
            wrappers.append(schema_tool(tool_function))
        if wrappers:
            await self._session.add_tools(wrappers)

    def _messages(self, messages: List[Dict[str, Any]]) -> List[Any]:
        import uzu

        converted = []
        for item in messages:
            role = (item.get("role") or "user").lower()
            if role == "tool":
                # Uzu rejects plain text on tool-role messages; results must be
                # ToolCallResult blocks tied to the call they answer.
                result = uzu.ChatContentBlock.ToolCallResult(
                    item.get("id") or item.get("tool_call_id") or None,
                    item.get("tool_name") or None,
                    uzu.Value(json.dumps(str(item.get("content") or ""))),
                )
                converted.append(uzu.ChatMessage.tool().with_block(result))
                continue
            if role == "system":
                message = uzu.ChatMessage.system()
            elif role == "assistant":
                message = uzu.ChatMessage.assistant()
            else:
                message = uzu.ChatMessage.user()

            content = item.get("content")
            if content:
                message = message.with_text(str(content))

            for call in item.get("tool_calls") or []:
                function = call.get("function") or {}
                arguments = function.get("arguments") or {}
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}
                arguments_value = uzu.Value(json.dumps(arguments))
                message = message.with_tool_call(
                    uzu.ToolCall(call.get("id") or None, function.get("name") or "", arguments_value)
                )
            converted.append(message)
        return converted

    def _reply_config(self, num_predict: Optional[int]) -> Any:
        import uzu

        # No automatic tool execution: the agent runs tools against its own
        # registry and context, so uzu should only emit the calls.
        return (
            uzu.ChatReplyConfig.create()
            .with_token_limit(num_predict or self.cfg.num_predict)
            .with_tool_turn_limit(0)
        )

    @staticmethod
    def _plain_call(call: Any) -> Dict[str, Any]:
        arguments = getattr(call, "arguments", {}) or {}
        if hasattr(arguments, "json"):
            arguments_text = arguments.json
            try:
                arguments = json.loads(arguments_text) if arguments_text else {}
            except json.JSONDecodeError:
                arguments = {"__invalid_json__": arguments_text[:300]}
        return {
            "id": getattr(call, "identifier", None) or "",
            "function": {
                "name": getattr(call, "name", "") or "",
                "arguments": arguments,
            },
        }

    @staticmethod
    def _is_tool_turn_error(error: Any) -> bool:
        return "tool turn limit" in str(error).lower()

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
             temperature: Optional[float] = None, num_predict: Optional[int] = None) -> LLMReply:
        # Uzu's non-streaming reply() discards the tool call when tool_turn_limit
        # is 0, so use the stream internally and simply drop the token callback.
        uzu_messages = self._messages(messages)
        return self._run(self._reply_stream(
            uzu_messages, self._reply_config(num_predict), lambda _token: None, tools
        ))

    async def _reply_stream(self, messages: List[Any], reply_config: Any,
                            on_token: TokenCallback,
                            tools: Optional[List[Dict[str, Any]]],
                            on_stats: Optional[Any] = None) -> LLMReply:
        import uzu

        await self._prepare(tools)
        stream = await self._session.reply_with_stream(messages, reply_config)
        parts: List[str] = []
        calls: List[Dict[str, Any]] = []
        live: Dict[str, Any] = {
            "prompt_tokens": None, "output_tokens": None, "tokens_per_second": None,
            "time_to_first_token": None, "prefill_tokens_per_second": None, "duration": None,
        }
        previous_text = ""
        async for chunk in stream.iterator():
            if isinstance(chunk, uzu.ChatSessionStreamChunk.Replies):
                replies = chunk.replies
                if replies:
                    reply = replies[0]
                    message = reply.message
                    if getattr(message, "text", None):
                        text = message.text
                        if text.startswith(previous_text):
                            delta = text[len(previous_text):]
                        else:
                            delta = text
                        previous_text = text
                        if delta:
                            parts.append(delta)
                            on_token(delta)
                    if getattr(message, "tool_calls", None):
                        calls = [self._plain_call(call) for call in message.tool_calls]
                    stats = getattr(reply, "stats", None)
                    # Stats fill in progressively; keep the latest non-null value.
                    for key, name in (
                        ("prompt_tokens", "tokens_count_input"),
                        ("output_tokens", "tokens_count_output"),
                        ("tokens_per_second", "generate_tokens_per_second"),
                        ("time_to_first_token", "time_to_first_token"),
                        ("prefill_tokens_per_second", "prefill_tokens_per_second"),
                        ("duration", "duration"),
                    ):
                        value = getattr(stats, name, None)
                        if value is not None:
                            live[key] = value
                    if on_stats:
                        on_stats(dict(live))
            elif isinstance(chunk, uzu.ChatSessionStreamChunk.Error):
                # tool_turn_limit=0 intentionally stops uzu before execution;
                # uzu reports that stop as an error after the call is emitted.
                if self._is_tool_turn_error(chunk.error):
                    continue
                raise LLMError(f"Mirai/Uzu stream failed: {chunk.error}")
        return LLMReply(
            {"role": "assistant", "content": "".join(parts), "tool_calls": calls},
            live["prompt_tokens"],
            live["output_tokens"],
            tokens_per_second=live["tokens_per_second"],
            time_to_first_token=live["time_to_first_token"],
            prefill_tokens_per_second=live["prefill_tokens_per_second"],
            duration=live["duration"],
        )

    def chat_stream(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, *,
                    on_token: TokenCallback, temperature: Optional[float] = None,
                    num_predict: Optional[int] = None, on_stats: Optional[Any] = None) -> LLMReply:
        uzu_messages = self._messages(messages)
        return self._run(self._reply_stream(
            uzu_messages, self._reply_config(num_predict), on_token, tools, on_stats
        ))

    def close(self) -> None:
        """Stop the background engine loop (used when switching models/providers)."""
        loop, thread = self._loop, self._thread
        if loop is not None and loop.is_running():
            loop.call_soon_threadsafe(loop.stop)
        if thread is not None and thread.is_alive():
            thread.join(timeout=2)
        self._session = None
        self._model = None
        self._engine = None
        self._loop = None
        self._thread = None
