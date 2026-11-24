"""Modular Intelligent Agent v2 package.

Import surface kept compatible with the original single-file script:

    Config, TokenCounter, SessionStore, FileRecord, FileTracker, WorkingState,
    ToolError, ToolResult, Toolbox, TOOL_SPECS, ContextManager, ContextTraceEvent,
    Limits, LLMError, LLMReply, OllamaLLM, IntelligentAgent, main,
    BASE_PROMPT, SUMMARIZER_SYSTEM, helpers and file constants.
"""

from .agent import IntelligentAgent
from .config import Config
from .context.limits import Limits
from .context.manager import ContextManager
from .context.prompts import BASE_PROMPT, SUMMARIZER_SYSTEM
from .context.token_counter import TokenCounter
from .context.trace import ContextTraceEvent
from .llm.errors import LLMError
from .llm.ollama import OllamaLLM
from .llm.llama_cpp import LlamaCppLLM
from .llm.mirai import MiraiLLM
from .llm.provider import create_llm
from .llm.reply import LLMReply
from .llm.streaming import LiveTokenMeter, StreamPrinter, ThinkFilter, TokenCallback
from .state.file_tracker import FileRecord, FileTracker
from .state.working_state import WorkingState
from .storage.session_store import SessionStore
from .tools.constants import LINE_CAP, MAX_READ_BYTES, MAX_SEARCH_FILE_BYTES, SKIP_DIRS
from .tools.bash import BashTool
from .tools.context import ToolExecutionContext
from .tools.filesystem import FileSystemTools
from .tools.memory import MemoryTools
from .tools.registry import Toolbox
from .tools.result import ToolError, ToolResult
from .tools.search import SearchTools
from .tools.specs import TOOL_SPECS
from .tools.web import WebTools
from .utilities.file_text import decode_text_file, encode_text_file
from .utilities.files import atomic_write_bytes, file_version, merge_ranges, path_key
from .utilities.formatting import fmt_size
from .utilities.html_text import HtmlTextExtractor
from .utilities.text import around, clip, head_tail, short_args, strip_think

__all__ = [
    "around", "atomic_write_bytes", "BASE_PROMPT", "BashTool", "clip", "Config", "ContextManager", "ContextTraceEvent",
    "decode_text_file", "encode_text_file", "FileRecord", "FileSystemTools", "FileTracker", "file_version",
    "fmt_size", "head_tail", "HtmlTextExtractor", "IntelligentAgent", "LINE_CAP", "Limits", "LLMError",
    "LLMReply", "LlamaCppLLM", "MiraiLLM", "create_llm", "LiveTokenMeter", "main", "MAX_READ_BYTES", "MAX_SEARCH_FILE_BYTES", "MemoryTools", "merge_ranges",
    "OllamaLLM", "path_key", "SearchTools", "SessionStore", "short_args", "SKIP_DIRS", "strip_think",
    "SUMMARIZER_SYSTEM", "StreamPrinter", "ThinkFilter", "TokenCallback", "TokenCounter", "Toolbox",
    "ToolError", "ToolExecutionContext", "ToolResult",
    "TOOL_SPECS", "WebTools", "WorkingState",
]


def __getattr__(name):
    if name == "main":
        from .cli import main
        return main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
