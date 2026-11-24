"""File-system primitives: range merging, atomic writes, versions and path keys."""

from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
from typing import List, Optional


def merge_ranges(ranges: List[List[int]]) -> List[List[int]]:
    out: List[List[int]] = []
    for start, end in sorted([list(r) for r in ranges]):
        if out and start <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out


def atomic_write_bytes(path: str, data: bytes) -> None:
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".agent_tmp_", dir=directory)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        if os.path.exists(path):
            try:
                shutil.copymode(path, tmp)
            except OSError:
                pass
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def file_version(path: str) -> Optional[str]:
    """Cheap change detector: size + mtime. None when the file does not exist."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    return hashlib.sha1(f"{st.st_size}:{st.st_mtime_ns}".encode()).hexdigest()[:8]


def path_key(path: str) -> str:
    return os.path.normcase(os.path.abspath(path))
