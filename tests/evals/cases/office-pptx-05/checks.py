from __future__ import annotations
import re
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def check(ctx):
    pptx = ctx.workspace.root / "Monolith_to_Events_Pitch.pptx"
    if not pptx.is_file():
        return [CheckResult("pptx_exists", False, "Monolith_to_Events_Pitch.pptx not found")]
    with zipfile.ZipFile(pptx, "r") as zf:
        slides = sorted(n for n in zf.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n))
        text = " ".join(
            t.strip()
            for n in slides
            for t in ET.fromstring(zf.read(n)).itertext()
            if t and t.strip()
        ).lower()
    return [
        CheckResult("slide_count_6", len(slides) == 6, f"found {len(slides)} slides"),
        CheckResult("top_bottlenecks", "2480" in text and "1920" in text, "top-2 p99 latencies cited"),
        CheckResult("dba_objection_addressed", "outbox" in text and ("bloat" in text or "ttl" in text or "cleanup" in text or "partition" in text), "DBA outbox bloat risk addressed"),
        CheckResult("security_objection_addressed", "pii" in text and ("encrypt" in text or "kms" in text), "Security PII encryption risk addressed"),
    ]
