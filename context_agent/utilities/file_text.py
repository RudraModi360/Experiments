"""Text-file decoding/encoding that preserves newline style and a UTF-8 BOM."""

from __future__ import annotations

from typing import Tuple

from ..tools.result import ToolError


def decode_text_file(path: str) -> Tuple[str, str, bool]:
    """Returns (text with \\n endings, original newline style, had_bom). Refuses binary / non-UTF-8."""
    with open(path, "rb") as handle:
        raw = handle.read()
    if b"\x00" in raw[:8192]:
        raise ToolError("binary file; cannot edit as text")
    bom = raw.startswith(b"\xef\xbb\xbf")
    if bom:
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ToolError("file is not valid UTF-8; refusing to edit it to avoid corruption") from exc
    crlf = text.count("\r\n")
    newline = "\r\n" if crlf > text.count("\n") - crlf else "\n"
    return text.replace("\r\n", "\n"), newline, bom


def encode_text_file(text: str, newline: str, bom: bool) -> bytes:
    if newline == "\r\n":
        text = text.replace("\n", "\r\n")
    data = text.encode("utf-8")
    return (b"\xef\xbb\xbf" + data) if bom else data
