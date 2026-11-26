from __future__ import annotations
import re
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def check(ctx):
    pptx = ctx.workspace.root / "Sprint_14_Update.pptx"
    if not pptx.is_file():
        return [CheckResult("pptx_exists", False, "Sprint_14_Update.pptx not found")]
    with zipfile.ZipFile(pptx, "r") as zf:
        slides = sorted(n for n in zf.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n))
        text = " ".join(
            t.strip() for n in slides for t in ET.fromstring(zf.read(n)).itertext() if t and t.strip()
        )
    return [
        CheckResult("slide_count_5", len(slides) == 5, f"found {len(slides)} slides"),
        CheckResult("points_34_and_13", "34" in text and "13" in text, "34 completed / 13 carryover points"),
        CheckResult("blockers_listed", "ENG-412" in text and "ENG-419" in text, "both blockers listed"),
    ]
