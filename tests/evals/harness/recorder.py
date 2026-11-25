"""Instrumentation that records tool calls and emits DeepEval tool spans.

The application code is untouched: the harness subclasses ``Toolbox`` and
``IntelligentAgent`` and swaps in a recording toolbox after construction. Each
tool call becomes a child span of the active agent span, which is what
``StepEfficiencyMetric`` and ``ToolCorrectnessMetric`` read.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from context_agent.agent import IntelligentAgent
from context_agent.tools.registry import Toolbox
from context_agent.tools.result import ToolResult
from deepeval.tracing import observe, update_current_span

GROUNDING_TOOLS = {"read_file", "search_text", "web_search", "fetch_url"}
MAX_GROUNDING_ITEMS = 20
MAX_GROUNDING_CHARS = 2000


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    return str(value)


@dataclass
class ToolCallRecord:
    name: str
    args: dict[str, Any]
    output: str
    ok: bool = True
    meta: dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "args": _jsonable(self.args),
            "output": self.output,
            "ok": self.ok,
            "meta": _jsonable(self.meta),
            "duration": round(self.duration, 4),
        }


@dataclass
class ToolPolicy:
    allow: set[str] = field(default_factory=set)
    deny: set[str] = field(default_factory=set)
    network: bool = False
    bash: bool = True

    def allows(self, name: str) -> bool:
        if name in self.deny:
            return False
        if name == "bash" and not self.bash:
            return False
        if name in {"web_search", "fetch_url"} and not self.network:
            return False
        if self.allow and name not in self.allow:
            return False
        return True


def build_policy(case) -> ToolPolicy:
    spec = case.workspace
    return ToolPolicy(
        allow=set(spec.allow_tools),
        deny=set(spec.deny_tools),
        network=bool(spec.network),
        bash=bool(spec.bash),
    )


class Recorder:
    """Collects the agent's observable behavior for checks and reports."""

    def __init__(
        self,
        on_tool: Callable[[str, bool], None] | None = None,
    ) -> None:
        self.tool_calls: list[ToolCallRecord] = []
        self.history: list[dict[str, Any]] = []
        self.agent: IntelligentAgent | None = None
        self.on_tool = on_tool

    def record(self, name: str, args: Any, result: ToolResult, duration: float) -> None:
        self.tool_calls.append(
            ToolCallRecord(
                name=name,
                args=args if isinstance(args, dict) else {"value": args},
                output=result.text,
                ok=bool(result.ok),
                meta=dict(result.meta or {}),
                duration=duration,
            )
        )
        if self.on_tool is not None:
            try:
                self.on_tool(name, bool(result.ok))
            except Exception:
                # Progress reporting must never break a case.
                pass

    def sync_last(self, name: str, result: ToolResult) -> None:
        if self.tool_calls and self.tool_calls[-1].name == name:
            self.tool_calls[-1].output = result.text
            self.tool_calls[-1].ok = bool(result.ok)

    def attach(self, agent: IntelligentAgent) -> None:
        self.agent = agent

    def capture_history(self) -> list[dict[str, Any]]:
        if self.agent is not None:
            try:
                self.history = [
                    self.agent.ctx.public(message) for message in self.agent.ctx.history
                ]
            except Exception:
                self.history = []
        return self.history

    def retrieval_context(self) -> list[str]:
        """Build grounding context from what the agent actually read."""
        seen: set[str] = set()
        items: list[str] = []
        for record in self.tool_calls:
            if record.name not in GROUNDING_TOOLS or not record.ok:
                continue
            text = (record.output or "").strip()
            if not text:
                continue
            digest = text[:200]
            if digest in seen:
                continue
            seen.add(digest)
            items.append(text[:MAX_GROUNDING_CHARS])
            if len(items) >= MAX_GROUNDING_ITEMS:
                break
        return items


def make_traced_runner(toolbox: Toolbox):
    """Return a tool runner that creates one child span per call.

    The closure keeps the non-serializable toolbox out of the span arguments;
    the span receives only the tool name, arguments and output.
    """

    @observe(type="tool")
    def run(name: str, args: Any, cap: int) -> ToolResult:
        result = Toolbox.run(toolbox, name, args, cap)
        update_current_span(
            name=name,
            input=_jsonable(args),
            output=result.text,
            metadata={"ok": bool(result.ok), **_jsonable(result.meta or {})},
        )
        return result

    return run


class RecordingToolbox(Toolbox):
    """A Toolbox that filters tools by policy and records every call."""

    def __init__(self, cfg, files, state, store, *, recorder: Recorder, policy: ToolPolicy):
        super().__init__(cfg, files, state, store)
        self.recorder = recorder
        self.policy = policy

        allowed = {
            schema["function"]["name"]
            for schema in self.schemas
            if policy.allows(schema["function"]["name"])
        }
        self.schemas = [
            schema for schema in self.schemas
            if schema["function"]["name"] in allowed
        ]
        self._params = {name: value for name, value in self._params.items() if name in allowed}
        self._handlers = {name: value for name, value in self._handlers.items() if name in allowed}
        self._traced_run = make_traced_runner(self)

    def run(self, name: str, args: Any, cap: int) -> ToolResult:
        if not self.policy.allows(name):
            result = ToolResult(
                f"Tool '{name}' is disabled for this evaluation. "
                f"Available: {', '.join(sorted(self._handlers))}",
                ok=False,
            )
            self.recorder.record(name, args, result, 0.0)
            return result
        started = time.monotonic()
        result = self._traced_run(name, args, cap)
        self.recorder.record(name, args, result, time.monotonic() - started)
        return result


class EvalAgent(IntelligentAgent):
    """An ``IntelligentAgent`` whose toolbox is replaced by the recorder."""

    def __init__(self, cfg, recorder: Recorder, policy: ToolPolicy, *,
                 on_step: Callable[[int], None] | None = None, **kwargs):
        super().__init__(cfg, **kwargs)
        self._on_step = on_step
        # ContextManager only uses the schemas for a token estimate, so replacing
        # the toolbox after construction is safe.
        self.tools = RecordingToolbox(
            self.cfg,
            self.files,
            self.state,
            self.store,
            recorder=recorder,
            policy=policy,
        )
        orig_add = self.ctx.add_tool_result

        def _tracked_add_tool_result(name, args, res):
            recorder.sync_last(name, res)
            return orig_add(name, args, res)

        self.ctx.add_tool_result = _tracked_add_tool_result
        recorder.attach(self)

    def _record_stats(self, reply) -> None:
        super()._record_stats(reply)
        if self._on_step is not None:
            try:
                self._on_step(int((self.last_stats or {}).get("steps") or 0))
            except Exception:
                pass
