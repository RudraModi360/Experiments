from __future__ import annotations
import re
from tests.evals.harness.checks import CheckResult


def _extract_pdf(path):
    try:
        from pypdf import PdfReader
        r = PdfReader(str(path))
        return len(r.pages), "\n".join((p.extract_text() or "") for p in r.pages)
    except Exception:
        raw = path.read_bytes().decode("latin-1", "replace")
        return max(1, len(re.findall(r"/Type\s*/Page\b", raw))), raw


def check(ctx):
    pdf = ctx.workspace.root / "Europe_Trip_Itinerary.pdf"
    if not pdf.is_file():
        return [CheckResult("pdf_exists", False, "Europe_Trip_Itinerary.pdf not found")]
    pages, text = _extract_pdf(pdf)
    low = text.lower()
    return [
        CheckResult("valid_pdf", pdf.read_bytes()[:5] == b"%PDF-", f"pages={pages}"),
        CheckResult("cities_and_refs", "hox-771" in low and "stg-204" in low and "lh902" in low, "hotel & flight refs included"),
        CheckResult("per_diem_caps", "85" in low and "75" in low, "London 85 and Frankfurt 75 per-diem caps"),
        CheckResult("timezone_overlap_flagged", ("overlap" in low or "conflict" in low) and "berlin" in low, "flags 15:00 GMT vs 16:00 CET overlap"),
        CheckResult("tight_transfer_flagged", ("35" in low or "14:25" in low) and ("conflict" in low or "tight" in low or "buffer" in low or "impossible" in low), "flags 35-min FRA landing-to-meeting conflict"),
    ]
