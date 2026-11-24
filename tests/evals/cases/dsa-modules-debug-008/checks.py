"""Evidence: required complexities preserved (no O(n) scans in LRU ops)."""
import re
from pathlib import Path

from tests.evals.harness.checks import CheckResult


def _body(src, name):
    m = re.search(rf"def {name}\(.*?\):(.*?)(?=\n    def |\nclass |\Z)", src, re.S)
    return m.group(1) if m else ""


def check(ctx):
    root = Path(ctx.workspace.root) / "repo"
    lru = (root / "lru.py").read_text(encoding="utf-8") if (root / "lru.py").exists() else ""
    intervals = (root / "intervals.py").read_text(encoding="utf-8") if (root / "intervals.py").exists() else ""

    get_body = _body(lru, "get")
    put_body = _body(lru, "put")
    lru_scan = bool(re.search(r"\bfor\b|\bsorted\b|\.index\(", get_body + put_body))
    get_refreshes = "move_to_end" in get_body

    # merge should sort once then single pass; flag a nested for over intervals.
    nested = bool(re.search(r"for .*:\s*\n\s*for ", intervals))

    return [
        CheckResult("lru_ops_no_linear_scan", not lru_scan, f"linear_scan_in_get_put={lru_scan}"),
        CheckResult("lru_get_refreshes_recency", get_refreshes, f"move_to_end_in_get={get_refreshes}"),
        CheckResult("merge_single_pass", not nested, f"nested_loop={nested}"),
    ]
