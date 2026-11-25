"""LLM provider selection."""

from __future__ import annotations

import os
from dataclasses import replace
from typing import Any

from ..config import Config
from .errors import LLMError
from .llama_cpp import LlamaCppLLM
from .mirai import MiraiLLM
from .ollama import OllamaLLM

GOOGLE_PROVIDERS = {
    "google",
    "gemini",
    "google-ai-studio",
    "google_ai_studio",
    "aistudio",
}
GOOGLE_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"


def google_api_key(cfg: Config) -> str:
    """Return the first configured Google AI Studio key (cfg wins)."""
    if cfg.api_key:
        return cfg.api_key
    for name in (
        "GEMINI_API_KEY",
        "GOOGLE_AI_STUDIO_API_KEY",
        "GOOGLE_API_KEY",
    ):
        value = (os.environ.get(name) or "").strip()
        if value:
            return value
    return ""


def create_llm(cfg: Config) -> Any:
    provider = (cfg.provider or "ollama").strip().lower()
    aliases = {
        "llama_cpp": "llama-cpp",
        "llamacpp": "llama-cpp",
        "llama.cpp": "llama-cpp",
        "openai": "llama-cpp",
        "openai-compatible": "llama-cpp",
    }
    provider = aliases.get(provider, provider)
    if provider in GOOGLE_PROVIDERS:
        api_key = google_api_key(cfg)
        if not api_key:
            raise LLMError(
                "Google AI Studio needs GEMINI_API_KEY (or --api-key / AGENT_API_KEY)."
            )
        google_cfg = replace(
            cfg,
            provider="google",
            base_url=cfg.base_url or GOOGLE_BASE_URL,
            api_key=api_key,
        )
        return LlamaCppLLM(google_cfg, google=True)
    if provider in {"llama-cpp", "llamacpp"}:
        return LlamaCppLLM(cfg)
    if provider == "ollama":
        return OllamaLLM(cfg)
    if provider in {"mirai", "uzu"}:
        return MiraiLLM(cfg)
    raise LLMError(
        f"Unknown LLM provider '{cfg.provider}'. "
        "Use 'mirai', 'ollama', 'llama-cpp', or 'google'."
    )
