"""JSON schemas advertised to the model for every tool."""

from __future__ import annotations

from typing import Any, Dict, Tuple


def _spec(name: str, desc: str, props: Dict[str, Tuple[str, str]],
          required: Tuple[str, ...] = ()) -> Dict[str, Any]:
    return {"type": "function", "function": {
        "name": name, "description": desc,
        "parameters": {"type": "object",
                       "properties": {k: {"type": t, "description": d} for k, (t, d) in props.items()},
                       "required": list(required)}}}


TOOL_SPECS = [
    _spec("read_file", "Read a text file in pages, with line numbers. Use offset/limit to page; never needed for whole files.",
          {"path": ("string", "File path"), "offset": ("integer", "First line (1-based), default 1"),
           "limit": ("integer", "Max lines, default 200"),
           "start_char": ("integer", "For very long lines: column to start from, default 0")}, ("path",)),
    _spec("write_file", "Create a file, or overwrite one you have already read. Existing unread files need overwrite=true.",
          {"path": ("string", "File path"), "content": ("string", "Full file content"),
           "overwrite": ("boolean", "Allow replacing an existing file")}, ("path", "content")),
    _spec("edit_file", "Replace exact text in a file. old_content must be raw text (no line-number prefixes) and unique unless replace_all.",
          {"path": ("string", "File path"), "old_content": ("string", "Exact text to replace"),
           "new_content": ("string", "Replacement text"), "replace_all": ("boolean", "Replace every occurrence")},
          ("path", "old_content", "new_content")),
    _spec("search_text", "Regex search inside a file or directory tree. Returns file:line matches.",
          {"pattern": ("string", "Regex (falls back to literal)"), "path": ("string", "File or directory, default ."),
           "max_results": ("integer", "Default 30"), "context_lines": ("integer", "0-3 lines around each match"),
           "ignore_case": ("boolean", "Default true")}, ("pattern",)),
    _spec("search_files", "Find files whose NAME matches a regex.",
          {"pattern": ("string", "Regex on file name"), "directory": ("string", "Default ."),
           "max_results": ("integer", "Default 50")}, ("pattern",)),
    _spec("list_files", "List a directory (depth-limited, skips junk folders).",
          {"directory": ("string", "Default ."), "max_depth": ("integer", "Default 2"),
           "max_entries": ("integer", "Default 150")}),
    _spec("bash", "Run a non-interactive bash command; use for tests, builds, git and scripts. Returns combined output and exit code. Commands run with your user permissions.",
          {"command": ("string", "Bash command to run"), "cwd": ("string", "Working directory, default ."),
           "timeout": ("integer", "Seconds, default 30, max 300")}, ("command",)),
    _spec("web_search", "Search the web for current or external information.",
          {"query": ("string", "Search query"), "max_results": ("integer", "Default 5")}, ("query",)),
    _spec("fetch_url", "Download a web page as text. Returns the first page and saves the rest to a file you can page with read_file.",
          {"url": ("string", "http(s) URL")}, ("url",)),
    _spec("update_plan", "Update your plan/checklist ONLY on complex multi-phase tasks (skip on simple read/write tasks and never call after finishing). Stays visible every step.",
          {"plan": ("string", "Full plan text")}, ("plan",)),
    _spec("save_note", "Save a durable fact on long multi-source or multi-turn tasks that may compact (skip on short local tasks). Empty content deletes it.",
          {"key": ("string", "Short label"), "content": ("string", "The fact to remember")}, ("key", "content")),
]
