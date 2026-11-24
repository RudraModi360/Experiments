"""LLM-judge configuration with a sticky fallback chain.

The judge is deliberately separate from the agent under test. By default it
uses Google AI Studio's Gemini API and falls back, per test case, when a target
is rate-limited or unavailable:

    gemini-3.5-flash-lite -> gemma-4-31b-it -> gemma-4-26b-a4b-it
                          -> ollama/nemotron-3.5-bolt:e4b-64k

The final Ollama fallback is the safety net for a single test case when every
Google target fails. Fallback is sticky for the life of one judge instance (one
metric / one case), so a rate-limited target is not retried on every call.

This is a DeepEval-compatible model: it implements ``DeepEvalBaseLLM`` and
delegates ``generate`` / ``a_generate`` (with schema) to the active target,
preserving each target's ``(output, cost)`` return shape. Authentication errors
are fatal so a bad key is visible instead of silently scoring another model.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any, Optional

from deepeval.models import DeepEvalBaseLLM

from .serving import (
    FALLBACK_KINDS,
    classify_error,
    google_api_key,
)

JUDGE_PREFIX = "[eval-judge]"

DEFAULT_JUDGE_CHAIN = (
    "google:gemini-3.5-flash-lite",
    "google:gemma-4-31b-it",
    "google:gemma-4-26b-a4b-it",
    "ollama:nemotron-3.5-bolt:e4b-64k",
)
DEFAULT_OLLAMA_JUDGE = "nemotron-3.5-bolt:e4b-64k"
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"


def _log(message: str) -> None:
    stream = getattr(sys, "__stdout__", None) or sys.stdout
    try:
        print(message, file=stream, flush=True)
    except Exception:  # pragma: no cover
        pass


def _env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


@dataclass(frozen=True)
class JudgeTarget:
    provider: str
    model: str
    base_url: str = ""

    @property
    def label(self) -> str:
        return f"{self.provider}/{self.model}"


def _parse_chain(raw: str) -> list[JudgeTarget]:
    targets: list[JudgeTarget] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        provider, _, model = item.partition(":")
        provider = provider.strip().lower()
        model = model.strip()
        if not model:
            provider, model = "ollama", provider
        if provider in {"gemini", "google-ai-studio", "aistudio"}:
            provider = "google"
        targets.append(JudgeTarget(provider, model))
    return targets


def judge_chain() -> list[JudgeTarget]:
    """Resolve the effective judge chain from the environment.

    Precedence:
      1. ``EVAL_JUDGE_CHAIN`` (explicit ``provider:model`` list).
      2. ``EVAL_JUDGE_PROVIDER=ollama|local`` -> a single local judge.
      3. Default Gemini chain when a Google key is present, else Ollama only.
    """
    explicit = _env("EVAL_JUDGE_CHAIN")
    if explicit:
        return _parse_chain(explicit)

    provider = _env("EVAL_JUDGE_PROVIDER").lower()
    if provider in {"ollama", "local", "openai-compatible", "openai_compatible"}:
        model = _env("EVAL_JUDGE_MODEL", DEFAULT_OLLAMA_JUDGE)
        base_url = _env("EVAL_JUDGE_BASE_URL", DEFAULT_OLLAMA_BASE_URL)
        return [JudgeTarget("ollama" if provider == "ollama" else "local", model, base_url)]

    targets = _parse_chain(",".join(DEFAULT_JUDGE_CHAIN))
    if not google_api_key():
        # No Google key: keep only the local safety net.
        targets = [t for t in targets if t.provider != "google"]
    return targets or [JudgeTarget("ollama", DEFAULT_OLLAMA_JUDGE, DEFAULT_OLLAMA_BASE_URL)]


def describe_judge_chain() -> str:
    return " -> ".join(t.label for t in judge_chain())


def judge_settings() -> dict[str, Any]:
    """Effective judge configuration for reports."""
    return {
        "chain": [t.label for t in judge_chain()],
        "google_key_present": bool(google_api_key()),
    }


# Underlying DeepEval model objects are expensive-ish to build; cache them by
# target so a fresh per-case judge wrapper reuses the same clients.
_MODEL_CACHE: dict[tuple[str, str, str], Any] = {}


def _build_model(target: JudgeTarget) -> Any:
    key = (target.provider, target.model, target.base_url)
    if key in _MODEL_CACHE:
        return _MODEL_CACHE[key]

    if target.provider == "google":
        from deepeval.models import GeminiModel

        api_key = google_api_key()
        if not api_key:
            raise RuntimeError("Google judge target requires GEMINI_API_KEY / GOOGLE_API_KEY")
        model = GeminiModel(model=target.model, api_key=api_key, temperature=0.0)
    elif target.provider == "ollama":
        from deepeval.models import OllamaModel

        model = OllamaModel(
            model=target.model,
            base_url=target.base_url or DEFAULT_OLLAMA_BASE_URL,
            temperature=0.0,
        )
    elif target.provider in {"local", "openai-compatible", "openai_compatible"}:
        from deepeval.models import LocalModel

        model = LocalModel(
            model=target.model,
            base_url=target.base_url or DEFAULT_OLLAMA_BASE_URL,
            api_key=_env("EVAL_JUDGE_API_KEY", "local"),
            temperature=0.0,
        )
    else:
        raise RuntimeError(f"unsupported judge provider {target.provider!r}")

    _MODEL_CACHE[key] = model
    return model


def _reason(exc: BaseException) -> str:
    status = getattr(exc, "status", None) or getattr(exc, "code", None)
    if not isinstance(status, int):
        status = None
    return classify_error(status, str(exc))


class FallbackJudgeModel(DeepEvalBaseLLM):
    """A DeepEval judge that walks a sticky fallback chain on retryable errors."""

    def __init__(self, targets: Optional[list[JudgeTarget]] = None):
        self.targets = list(targets) if targets else judge_chain()
        if not self.targets:
            raise RuntimeError("empty judge chain")
        self.index = 0
        self.switches: list[dict[str, str]] = []
        _log(f"{JUDGE_PREFIX} chain: {' -> '.join(t.label for t in self.targets)}")

    # -- DeepEvalBaseLLM interface ------------------------------------------
    def load_model(self, *args, **kwargs) -> "FallbackJudgeModel":
        return self

    def get_model_name(self) -> str:
        return self.targets[self.index].label

    @property
    def supports_structured_outputs(self) -> bool:
        try:
            return bool(getattr(self._active(), "supports_structured_outputs", True))
        except Exception:
            return True

    def _active(self) -> Any:
        return _build_model(self.targets[self.index])

    def _advance(self, exc: BaseException) -> bool:
        """Move to the next target on a retryable error; return True if moved."""
        reason = _reason(exc)
        if reason in FALLBACK_KINDS and self.index < len(self.targets) - 1:
            previous = self.targets[self.index].label
            self.index += 1
            nxt = self.targets[self.index].label
            self.switches.append({"from": previous, "to": nxt, "reason": reason, "detail": str(exc)[:300]})
            _log(f"{JUDGE_PREFIX} {reason} on {previous}: {str(exc)[:160]} -> switching to {nxt}")
            return True
        return False

    def generate(self, prompt: str, schema: Any = None, **kwargs):
        while True:
            try:
                return self._active().generate_with_schema(prompt, schema=schema, **kwargs)
            except Exception as exc:
                if self._advance(exc):
                    continue
                raise

    async def a_generate(self, prompt: str, schema: Any = None, **kwargs):
        while True:
            try:
                return await self._active().a_generate_with_schema(prompt, schema=schema, **kwargs)
            except Exception as exc:
                if self._advance(exc):
                    continue
                raise


def judge() -> FallbackJudgeModel:
    """Build a fresh judge per call so fallback stickiness is per test case."""
    return FallbackJudgeModel()
