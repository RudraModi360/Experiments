"""Shared limits and directory exclusions for file/search tools."""

from __future__ import annotations

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".idea", ".vscode",
             ".mypy_cache", ".pytest_cache", ".cache", ".next"}
LINE_CAP = 1500                       # max characters of one line shown by read_file
MAX_READ_BYTES = 200 * 1024 * 1024
MAX_SEARCH_FILE_BYTES = 5 * 1024 * 1024
