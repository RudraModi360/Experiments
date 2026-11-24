#!/usr/bin/env python3
"""Intelligent Agent v2 - entry point.

The implementation now lives in the ``context_agent`` package, split by component:

    context_agent/
      config.py                     Config and budget defaults
      agent.py                      IntelligentAgent turn / tool loop
      cli.py                        command-line entry point
      llm/                          LLM adapters (Mirai/Uzu, Ollama, llama.cpp), reply and error types
      storage/                      session store (transcript, snapshot, spill files)
      state/                        file tracker and working state (ledger)
      tools/                        file, search, web, bash, memory tools + registry
      context/
        manager.py                  maintain() pipeline
        view.py                     model view / system prompt
        token_counter.py            approximate token counting
        limits.py                   prompt budget policy
        summarizer.py               rolling-summary and digest fallback
        strategies/
          repair.py                 tool-call/result repair
          freshness.py              STALE file reads
          dedupe.py                 duplicate / superseded outputs
          clear.py                  clear old outputs and shrink call args
          compact.py                fold old units into a summary
          emergency.py              no-LLM overflow fallback
      utilities/                    text, file and HTML helpers

This module re-exports the original public names so existing imports of
``agent`` keep working, then starts the same CLI as before.
"""

from __future__ import annotations

from context_agent import (
    BASE_PROMPT,
    BashTool,
    LINE_CAP,
    MAX_READ_BYTES,
    MAX_SEARCH_FILE_BYTES,
    SKIP_DIRS,
    SUMMARIZER_SYSTEM,
    Config,
    ContextManager,
    ContextTraceEvent,
    FileRecord,
    FileSystemTools,
    FileTracker,
    HtmlTextExtractor,
    IntelligentAgent,
    Limits,
    LLMError,
    LLMReply,
    LiveTokenMeter,
    MemoryTools,
    MiraiLLM,
    OllamaLLM,
    SearchTools,
    SessionStore,
    StreamPrinter,
    ThinkFilter,
    TokenCallback,
    TokenCounter,
    Toolbox,
    ToolError,
    ToolExecutionContext,
    ToolResult,
    TOOL_SPECS,
    WebTools,
    WorkingState,
    around,
    atomic_write_bytes,
    clip,
    decode_text_file,
    encode_text_file,
    file_version,
    fmt_size,
    head_tail,
    main,
    merge_ranges,
    path_key,
    short_args,
    strip_think,
)
from context_agent.llm.ollama import _field, _plain
from context_agent.tools.specs import _spec
from context_agent.utilities.html_text import HtmlTextExtractor as _TextExtractor
from context_agent.utilities.file_text import decode_text_file as _decode_for_edit
from context_agent.utilities.file_text import encode_text_file as _encode_text

__all__ = [
    "around", "atomic_write_bytes", "BASE_PROMPT", "BashTool", "clip", "Config", "ContextManager", "ContextTraceEvent",
    "decode_text_file", "encode_text_file", "FileRecord", "FileSystemTools", "FileTracker", "file_version",
    "fmt_size", "head_tail", "HtmlTextExtractor", "IntelligentAgent", "LINE_CAP", "Limits", "LLMError",
    "LLMReply", "LiveTokenMeter", "main", "MAX_READ_BYTES", "MAX_SEARCH_FILE_BYTES", "MemoryTools", "merge_ranges",
    "MiraiLLM", "OllamaLLM", "path_key", "SearchTools", "SessionStore", "short_args", "SKIP_DIRS", "strip_think",
    "SUMMARIZER_SYSTEM", "StreamPrinter", "ThinkFilter", "TokenCallback", "TokenCounter", "Toolbox",
    "ToolError", "ToolExecutionContext", "ToolResult",
    "TOOL_SPECS", "WebTools", "WorkingState",
]

if __name__ == "__main__":
    main()
