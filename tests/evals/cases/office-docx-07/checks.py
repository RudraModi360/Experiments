from __future__ import annotations
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def check(ctx):
    sow = ctx.workspace.root / "Final_SOW.docx"
    summary = ctx.workspace.root / "changes_summary.md"
    results = []
    if not sow.is_file():
        results.append(CheckResult("final_sow_exists", False, "Final_SOW.docx not found"))
    else:
        with zipfile.ZipFile(sow, "r") as zf:
            text = " ".join(t.strip() for t in ET.fromstring(zf.read("word/document.xml")).itertext() if t and t.strip())
        low = text.lower()
        results.append(CheckResult("fee_52000", "52,000" in low or "52000" in low, "updated Phase 1 fee $52,000"))
        results.append(CheckResult("net_30", "net-30" in low or "net 30" in low, "updated payment terms Net-30"))
        results.append(CheckResult("launch_2026_12_18", "2026-12-18" in low or "december 18" in low or "dec 18" in low, "updated launch date"))
        results.append(CheckResult("ip_clause_inserted", "client intellectual property upon full payment" in low, "mandatory IP clause inserted"))
        results.append(CheckResult("sso_added_mobile_deferred", "sso" in low and "phase 2" in low, "SSO added and Mobile App deferred to Phase 2"))
        results.append(CheckResult("no_placeholder", "[insert" not in low, "placeholder removed"))
    results.append(CheckResult("changes_summary_exists", summary.is_file() and summary.stat().st_size >= 80, "changes_summary.md created"))
    return results
