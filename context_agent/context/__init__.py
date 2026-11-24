"""Layered text-context engine: view, budget, summarizer and strategies."""

from .limits import BudgetPolicy, Limits
from .manager import ContextManager
from .message import clean_message, message_units, public_message, stub_message
from .prompts import BASE_PROMPT, SUMMARIZER_SYSTEM
from .summarizer import ContextSummarizer
from .token_counter import TokenCounter
from .trace import ContextTrace, ContextTraceEvent
from .view import ContextView

__all__ = [
    "BASE_PROMPT", "BudgetPolicy", "clean_message", "ContextManager", "ContextSummarizer", "ContextTrace",
    "ContextTraceEvent", "ContextView", "Limits", "message_units", "public_message", "stub_message",
    "SUMMARIZER_SYSTEM", "TokenCounter",
]
