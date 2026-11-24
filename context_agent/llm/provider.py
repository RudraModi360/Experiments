"""LLM provider selection."""

from __future__ import annotations

from typing import Any

from ..config import Config
from .errors import LLMError
from .llama_cpp import LlamaCppLLM
from .mirai import MiraiLLM
from .ollama import OllamaLLM


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
    if provider in {"llama-cpp", "llamacpp"}:
        return LlamaCppLLM(cfg)
    if provider == "ollama":
        return OllamaLLM(cfg)
    if provider in {"mirai", "uzu"}:
        return MiraiLLM(cfg)
    raise LLMError(
        f"Unknown LLM provider '{cfg.provider}'. Use 'mirai', 'ollama', or 'llama-cpp'."
    )
