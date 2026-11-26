"""Run one case inside a traced agent span and collect everything the report needs."""

from __future__ import annotations

import os
import signal
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from context_agent.config import Config
from deepeval.dataset import Golden
from deepeval.test_case import ConversationalTestCase, ToolCall, Turn
from deepeval.tracing import observe, update_current_trace

from .case import Case
from .recorder import EvalAgent, Recorder, ToolCallRecord, build_policy
from .serving import build_serving_llm
from .workspace import (
    Workspace,
    diff_manifests,
    diff_summary,
    snapshot_manifest,
)

# The agent under test defaults to the local uzu Qwen model (32k window). The
# judge is configured separately in harness/judge.py. Both are env-overridable.
DEFAULT_AGENT_MODEL = "trymirai/Qwen3.5-9B-M"
DEFAULT_AGENT_PROVIDER = "uzu"
DEFAULT_AGENT_NUM_CTX = 32768
TRUNCATION_MARKERS = (
    "Stopped early:",
    "step limit reached",
    "the same call kept repeating without progress",
    "I stopped because:",
)


@dataclass
class RunResult:
    case_id: str
    final_output: str
    tool_calls: list[ToolCallRecord] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    diff: dict[str, list[str]] = field(default_factory=dict)
    before: dict[str, dict[str, Any]] = field(default_factory=dict)
    after: dict[str, dict[str, Any]] = field(default_factory=dict)
    duration: float = 0.0
    steps: int = 0
    truncated: bool = False
    timed_out: bool = False
    error: str | None = None
    retrieval_context: list[str] = field(default_factory=list)
    transcript_path: str | None = None
    agent_home: str = ""
    workspace_root: str = ""
    model: str = ""
    provider: str = ""
    model_chain: list[str] = field(default_factory=list)
    fallbacks: list[dict[str, str]] = field(default_factory=list)
    setup_results: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "final_output": self.final_output,
            "tool_calls": [call.to_dict() for call in self.tool_calls],
            "diff": self.diff,
            "duration": round(self.duration, 3),
            "steps": self.steps,
            "truncated": self.truncated,
            "timed_out": self.timed_out,
            "error": self.error,
            "retrieval_context": self.retrieval_context,
            "transcript_path": self.transcript_path,
            "workspace_root": self.workspace_root,
            "model": self.model,
            "provider": self.provider,
            "model_chain": self.model_chain,
            "fallbacks": self.fallbacks,
        }


class _TimeLimit:
    """Wall-clock limit around the agent run.

    Uses SIGALRM (main thread only) and raises ``KeyboardInterrupt`` so the
    agent's own ``except Exception`` blocks cannot swallow it. The agent already
    handles KeyboardInterrupt by repairing and saving context.
    """

    def __init__(self, seconds: float | None):
        self.seconds = float(seconds or 0)
        self.timed_out = False
        self._enabled = (
            self.seconds > 0
            and threading.current_thread() is threading.main_thread()
            and hasattr(signal, "SIGALRM")
        )
        self._previous = None

    def __enter__(self):
        if self._enabled:
            self._previous = signal.signal(signal.SIGALRM, self._handle)
            signal.setitimer(signal.ITIMER_REAL, self.seconds)
        return self

    def _handle(self, signum, frame):  # pragma: no cover - signal path
        self.timed_out = True
        raise KeyboardInterrupt

    def __exit__(self, exc_type, exc, tb):
        if self._enabled:
            signal.setitimer(signal.ITIMER_REAL, 0)
            if self._previous is not None:
                signal.signal(signal.SIGALRM, self._previous)
        return False


def _agent_config(case: Case, workspace: Workspace) -> Config:
    model = os.getenv("AGENT_MODEL", DEFAULT_AGENT_MODEL).strip()
    provider = os.getenv("AGENT_PROVIDER", DEFAULT_AGENT_PROVIDER).strip()
    base_url = os.getenv("AGENT_BASE_URL", "").strip() or None
    host = os.getenv("AGENT_HOST", "").strip() or None
    num_ctx = int(os.getenv("AGENT_NUM_CTX", str(DEFAULT_AGENT_NUM_CTX)))
    max_steps = case.workspace.max_steps or 25
    timeout = max(30.0, float(case.workspace.timeout_seconds or 300.0))
    return Config(
        model=model,
        provider=provider,
        base_url=base_url,
        host=host,
        num_ctx=num_ctx,
        temperature=float(case.workspace.temperature),
        max_steps_per_turn=int(max_steps),
        home=str(workspace.agent_home),
        verbose=False,
        request_timeout=timeout,
    )


def _steps_from_history(history: list[dict[str, Any]]) -> int:
    return sum(1 for message in history if message.get("role") == "assistant")


def _trace_tools(calls: list[ToolCallRecord]) -> list[ToolCall]:
    return [
        ToolCall(
            name=call.name,
            input_parameters=call.args,
            output=call.output,
        )
        for call in calls
    ]


def _trace_expected_tools(case: Case) -> list[ToolCall]:
    return [ToolCall(name=name) for name in case.expected_tools]


def _diff_context(case: Case, result: RunResult, checks: Any = None) -> list[str]:
    context: list[str] = []
    if result.diff:
        context.append("Workspace changes after the agent run:\n" + diff_summary(result.diff))
    if checks is not None:
        rows = []
        for command in getattr(checks, "command_results", []) or []:
            stdout = (command.get("stdout") or "").strip()
            stderr = (command.get("stderr") or "").strip()
            combined = stdout + (("\n" + stderr) if stderr else "")
            rows.append(
                f"$ {command.get('command')} (exit {command.get('exit_code')})\n"
                f"{combined[:2000]}"
            )
        if rows:
            context.append("Verification commands:\n" + "\n\n".join(rows))
        # Deterministic observations are EVIDENCE for the judge, not a gate.
        evidence = []
        for item in getattr(checks, "results", []) or []:
            if getattr(item, "kind", "") == "infra":
                continue
            mark = "ok" if getattr(item, "passed", False) else "ISSUE"
            detail = (getattr(item, "detail", "") or "")[:300]
            evidence.append(f"[{mark}] {getattr(item, 'name', '')}: {detail}")
        if evidence:
            context.append(
                "Deterministic evidence (for the judge to weigh, not an automatic gate):\n"
                + "\n".join(evidence[:40])
            )
    return context


def make_golden(case: Case, result: RunResult, checks: Any = None) -> Golden:
    context = list(case.context) + _diff_context(case, result, checks)
    retrieval = result.retrieval_context or case.retrieval_context
    return Golden(
        id=case.id,
        name=case.name,
        input=case.input,
        actual_output=result.final_output or None,
        expected_output=case.expected_output or None,
        context=context or None,
        retrieval_context=retrieval or None,
        tools_called=_trace_tools(result.tool_calls) or None,
        expected_tools=_trace_expected_tools(case) or None,
        additional_metadata={
            "profile": case.profile,
            "tags": case.tags,
            "difficulty": case.difficulty,
            "model": result.model,
            "provider": result.provider,
            "model_chain": result.model_chain,
            "fallbacks": result.fallbacks,
            **case.metadata,
        },
    )


@observe(type="agent")
def run_traced_case(
    case: Case, workspace: Workspace, progress: Any = None
) -> RunResult:
    """Run one case as a child of an agent span.

    The trace carries everything DeepEval's metrics read: input, expected
    output, context, retrieval context, tools called and expected tools.
    ``progress`` is an optional live-status object (``CaseProgress``) that is
    fed the agent's step and tool events so the terminal can show which case is
    running.
    """
    retrieval = (
        list(case.retrieval_context)
        if case.grounding == "static" and case.retrieval_context
        else None
    )
    update_current_trace(
        name=case.id,
        tags=case.tags or None,
        metadata={
            "profile": case.profile,
            "difficulty": case.difficulty,
            "grounding": case.grounding,
            **case.metadata,
        },
        input=case.input,
        expected_output=case.expected_output or None,
        context=case.context or None,
        retrieval_context=retrieval,
        expected_tools=_trace_expected_tools(case) or None,
    )

    if progress is not None:
        progress.set_phase("agent")
    cfg = _agent_config(case, workspace)
    serving = build_serving_llm(cfg)
    if serving is not None:
        # Google AI Studio free models expose a 16k window; keep the context
        # budget inside the smallest serving target so a fallback cannot
        # suddenly see an over-long prompt.
        cfg.num_ctx = serving.num_ctx
    recorder = Recorder(on_tool=progress.on_tool if progress is not None else None)
    policy = build_policy(case)
    agent = EvalAgent(
        cfg,
        recorder,
        policy=policy,
        llm=serving,
        on_step=progress.on_step if progress is not None else None,
    )

    previous_cwd = Path.cwd()
    previous_addopts = os.environ.get("PYTEST_ADDOPTS")
    addopts = previous_addopts or ""
    if "no:deepeval" not in addopts:
        # The agent's bash tool inherits this; keep DeepEval's pytest plugin out
        # of sandbox test runs without touching the outer eval process.
        os.environ["PYTEST_ADDOPTS"] = (addopts + " -p no:deepeval").strip()

    started = time.monotonic()
    timed_out = False
    error: str | None = None
    final_output = ""
    try:
        os.chdir(workspace.root)
        with _TimeLimit(case.workspace.timeout_seconds) as limit:
            final_output = agent.process_query(case.input)
        timed_out = limit.timed_out
    except Exception as exc:  # the agent normally handles its own errors
        error = f"{type(exc).__name__}: {exc}"
        final_output = ""
    finally:
        os.chdir(previous_cwd)
        if previous_addopts is None:
            os.environ.pop("PYTEST_ADDOPTS", None)
        else:
            os.environ["PYTEST_ADDOPTS"] = previous_addopts

    duration = time.monotonic() - started
    history = recorder.capture_history()
    after = snapshot_manifest(workspace.root)
    diff = diff_manifests(workspace.before, after)

    if timed_out:
        error = error or f"agent run exceeded {case.workspace.timeout_seconds:.0f}s"
    truncated = timed_out or any(marker in final_output for marker in TRUNCATION_MARKERS)

    grounding = recorder.retrieval_context() if case.grounding == "tool_outputs" else []
    if case.grounding == "static":
        grounding = list(case.retrieval_context)

    transcript_path = None
    try:
        candidate = Path(agent.store.dir) / "transcript.jsonl"
        if candidate.is_file():
            transcript_path = str(candidate)
    except Exception:
        transcript_path = None

    if serving is not None:
        active = serving.active
        model = active.model
        provider = active.provider
        model_chain = [target.label for target in serving.targets]
        fallbacks = list(serving.switches)
    else:
        model = cfg.model
        provider = cfg.provider
        model_chain = [f"{cfg.provider}/{cfg.model}"]
        fallbacks = []

    result = RunResult(
        case_id=case.id,
        final_output=final_output,
        tool_calls=list(recorder.tool_calls),
        history=history,
        diff=diff,
        before=workspace.before,
        after=after,
        duration=duration,
        steps=(agent.last_stats or {}).get("steps") or _steps_from_history(history),
        truncated=truncated,
        timed_out=timed_out,
        error=error,
        retrieval_context=grounding,
        transcript_path=transcript_path,
        agent_home=str(workspace.agent_home),
        workspace_root=str(workspace.root),
        model=model,
        provider=provider,
        model_chain=model_chain,
        fallbacks=fallbacks,
        setup_results=list(workspace.setup_results),
    )

    update_current_trace(
        output=result.final_output,
        tools_called=_trace_tools(result.tool_calls) or None,
        retrieval_context=result.retrieval_context or None,
        metadata={
            "steps": result.steps,
            "duration": round(result.duration, 3),
            "truncated": result.truncated,
            "timed_out": result.timed_out,
            "tool_errors": sum(1 for call in result.tool_calls if not call.ok),
            "model": result.model,
            "provider": result.provider,
            "fallbacks": len(result.fallbacks),
        },
    )
    return result


@observe(type="agent")
def run_traced_conversation(
    case: Case, workspace: Workspace, progress: Any = None
) -> tuple[ConversationalTestCase, RunResult]:
    """Run a scripted multi-turn case on one persistent agent session.

    Each ``user`` turn is sent to ``process_query`` on the same agent, so the
    session history, summary, notes and file tracker carry across turns. The
    resulting ``ConversationalTestCase`` is scored with conversational metrics.
    ``progress`` is fed cumulative step and tool events for the live status.
    """
    update_current_trace(
        name=case.id,
        tags=case.tags or None,
        metadata={"profile": case.profile, "difficulty": case.difficulty, "multi_turn": True, **case.metadata},
        input=str(case.turns[0].get("content", "")) if case.turns else case.input,
        expected_output=case.expected_outcome or None,
    )

    if progress is not None:
        progress.set_phase("agent")
    cfg = _agent_config(case, workspace)
    serving = build_serving_llm(cfg)
    if serving is not None:
        cfg.num_ctx = serving.num_ctx
    recorder = Recorder(on_tool=progress.on_tool if progress is not None else None)
    policy = build_policy(case)
    step_base = {"total": 0}

    def _on_step(turn_steps: int) -> None:
        if progress is not None:
            progress.on_step(step_base["total"] + int(turn_steps))

    agent = EvalAgent(
        cfg,
        recorder,
        policy=policy,
        llm=serving,
        on_step=_on_step if progress is not None else None,
    )

    previous_cwd = Path.cwd()
    previous_addopts = os.environ.get("PYTEST_ADDOPTS")
    addopts = previous_addopts or ""
    if "no:deepeval" not in addopts:
        os.environ["PYTEST_ADDOPTS"] = (addopts + " -p no:deepeval").strip()

    turns: list[Turn] = []
    started = time.monotonic()
    timed_out = False
    error: str | None = None
    last_output = ""
    total_steps = 0
    try:
        os.chdir(workspace.root)
        with _TimeLimit(case.workspace.timeout_seconds) as limit:
            for turn in case.turns:
                role = str(turn.get("role", "user")).strip().lower()
                content = str(turn.get("content", ""))
                if role == "assistant":
                    if turns and turns[-1].role == "assistant":
                        continue
                    # Scripted assistant context: inject without a model call.
                    agent.ctx.add({"role": "assistant", "content": content})
                    turns.append(Turn(role="assistant", content=content))
                    last_output = content
                    continue
                turns.append(Turn(role="user", content=content))
                last_output = agent.process_query(content)
                total_steps += (agent.last_stats or {}).get("steps", 0)
                step_base["total"] = total_steps
                turns.append(Turn(role="assistant", content=last_output))
        timed_out = limit.timed_out
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    finally:
        os.chdir(previous_cwd)
        if previous_addopts is None:
            os.environ.pop("PYTEST_ADDOPTS", None)
        else:
            os.environ["PYTEST_ADDOPTS"] = previous_addopts

    duration = time.monotonic() - started
    history = recorder.capture_history()
    after = snapshot_manifest(workspace.root)
    diff = diff_manifests(workspace.before, after)
    if timed_out:
        error = error or f"conversation exceeded {case.workspace.timeout_seconds:.0f}s"
    truncated = timed_out or any(marker in last_output for marker in TRUNCATION_MARKERS)
    grounding = recorder.retrieval_context() if case.grounding == "tool_outputs" else list(case.retrieval_context)

    transcript_path = None
    try:
        candidate = Path(agent.store.dir) / "transcript.jsonl"
        if candidate.is_file():
            transcript_path = str(candidate)
    except Exception:
        transcript_path = None

    if serving is not None:
        model, provider = serving.active.model, serving.active.provider
        model_chain = [t.label for t in serving.targets]
        fallbacks = list(serving.switches)
    else:
        model, provider = cfg.model, cfg.provider
        model_chain, fallbacks = [f"{cfg.provider}/{cfg.model}"], []

    result = RunResult(
        case_id=case.id,
        final_output=last_output,
        tool_calls=list(recorder.tool_calls),
        history=history,
        diff=diff,
        before=workspace.before,
        after=after,
        duration=duration,
        steps=total_steps or _steps_from_history(history),
        truncated=truncated,
        timed_out=timed_out,
        error=error,
        retrieval_context=grounding,
        transcript_path=transcript_path,
        agent_home=str(workspace.agent_home),
        workspace_root=str(workspace.root),
        model=model,
        provider=provider,
        model_chain=model_chain,
        fallbacks=fallbacks,
        setup_results=list(workspace.setup_results),
    )

    test_case = ConversationalTestCase(
        turns=turns,
        expected_outcome=case.expected_outcome or None,
        context=list(case.context) or None,
        retrieval_context=grounding or None,
        tags=case.tags or None,
        metadata={"case_id": case.id, "profile": case.profile, "model": model, **case.metadata},
    )
    update_current_trace(
        output=last_output,
        tools_called=_trace_tools(result.tool_calls) or None,
        metadata={"steps": result.steps, "turns": len(turns), "duration": round(duration, 3),
                  "truncated": truncated, "timed_out": timed_out, "model": model},
    )
    return test_case, result
