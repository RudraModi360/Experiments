from __future__ import annotations
import re
from tests.evals.harness.checks import CheckResult


def _extract_pdf_text(path):
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return len(reader.pages), "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        raw = path.read_bytes().decode("latin-1", "replace")
        pages = max(1, len(re.findall(r"/Type\s*/Page\b", raw)))
        return pages, raw


def check(ctx):
    pdf = ctx.workspace.root / "Vendor_Selection_Report.pdf"
    if not pdf.is_file():
        return [CheckResult("pdf_exists", False, "Vendor_Selection_Report.pdf not found")]
    header_ok = pdf.read_bytes()[:5] == b"%PDF-"
    pages, text = _extract_pdf_text(pdf)
    low = text.lower()
    return [
        CheckResult("valid_pdf_header", header_ok, f"pages={pages}"),
        CheckResult("recommends_beta", "beta" in low, "Vendor Beta referenced/recommended"),
        CheckResult("tco_figures_present", ("405,000" in low or "405k" in low) and ("480,000" in low or "480k" in low) and ("630,000" in low or "630k" in low), "all three 3-year TCO figures present"),
        CheckResult("alpha_eu_disqualified", "alpha" in low and ("eu" in low or "residency" in low), "Vendor Alpha EU residency blocker flagged"),
        CheckResult("gamma_over_budget", "gamma" in low and ("550,000" in low or "550k" in low or "budget" in low or "cap" in low), "Vendor Gamma budget cap violation flagged"),
    ]
