"""Text, formatting and file-system utilities."""

from .file_text import decode_text_file, encode_text_file
from .files import atomic_write_bytes, file_version, merge_ranges, path_key
from .formatting import fmt_size
from .html_text import HtmlTextExtractor
from .text import around, clip, head_tail, short_args, strip_think

__all__ = [
    "around", "atomic_write_bytes", "clip", "decode_text_file", "encode_text_file", "file_version",
    "fmt_size", "head_tail", "HtmlTextExtractor", "merge_ranges", "path_key", "short_args", "strip_think",
]
