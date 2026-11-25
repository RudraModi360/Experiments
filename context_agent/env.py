"""Minimal ``.env`` loader so the CLI can see repo keys without a dependency.

Only variables that are not already in the process environment are set, so an
explicit shell export always wins. The file format is the usual
``KEY=value`` / ``export KEY="value"`` subset; comments and blank lines are
ignored.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Iterator, Tuple

_LOADED: set[Path] = set()


def _candidates() -> Iterable[Path]:
    root = Path(__file__).resolve().parent.parent / ".env"
    yield root
    cwd = Path.cwd() / ".env"
    if cwd.resolve() != root.resolve():
        yield cwd


def _parse(text: str) -> Iterator[Tuple[str, str]]:
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key:
            yield key, value


def load_env_file(*paths: Path) -> None:
    """Load ``.env`` files without overriding existing environment values."""
    for path in paths or _candidates():
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in _LOADED:
            continue
        _LOADED.add(resolved)
        try:
            text = resolved.read_text(encoding="utf-8")
        except OSError:
            continue
        for key, value in _parse(text):
            os.environ.setdefault(key, value)


__all__ = ["load_env_file"]
