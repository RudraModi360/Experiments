from __future__ import annotations
import re
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def _extract_xml_text(data: bytes) -> str:
    root = ET.fromstring(data)
    return " ".join(t.strip() for t in root.itertext() if t and t.strip())


def check(ctx):
    pptx = ctx.workspace.root / "Q3_Board_Review.pptx"
    if not pptx.is_file():
        return [CheckResult("pptx_exists", False, "Q3_Board_Review.pptx not found")]
    results = []
    try:
        with zipfile.ZipFile(pptx, "r") as zf:
            names = zf.namelist()
            slides = sorted(n for n in names if re.match(r"^ppt/slides/slide\d+\.xml$", n))
            notes = sorted(n for n in names if re.match(r"^ppt/notesSlides/notesSlide\d+\.xml$", n))
            results.append(CheckResult("slide_count_8", len(slides) == 8, f"found {len(slides)} slides"))
            results.append(CheckResult("speaker_notes_gte_6", len(notes) >= 6, f"found {len(notes)} notes slides"))
            all_text = " ".join(_extract_xml_text(zf.read(n)) for n in slides + notes)
            low = all_text.lower()
            results.append(CheckResult("restated_arr_13_8", "13.8" in low, "checks restated $13.8M ARR"))
            results.append(CheckResult("deduped_pipeline_4_85", ("4.85" in low or "4,850,000" in low or "4850000" in low), "checks deduped $4.85M pipeline"))
            results.append(CheckResult("no_cobalt_leak", "cobalt" not in low, "Project Cobalt must not appear"))
            results.append(CheckResult("slipped_milestones_present", "sso" in low and "billing" in low, "mentions SSO v2 and Usage Billing API"))
    except Exception as exc:
        results.append(CheckResult("valid_pptx_zip", False, str(exc)))
    return results
