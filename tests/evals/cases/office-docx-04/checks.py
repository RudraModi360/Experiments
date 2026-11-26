from __future__ import annotations
import csv
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def check(ctx):
    docx = ctx.workspace.root / "Incident_2026_04_RCA.docx"
    actions = ctx.workspace.root / "action_items.csv"
    results = []
    if not docx.is_file():
        results.append(CheckResult("docx_exists", False, "Incident_2026_04_RCA.docx not found"))
    else:
        with zipfile.ZipFile(docx, "r") as zf:
            text = " ".join(t.strip() for t in ET.fromstring(zf.read("word/document.xml")).itertext() if t and t.strip())
        low = text.lower()
        for heading in ("executive summary", "incident timeline", "root cause analysis", "sla credits", "remediation"):
            results.append(CheckResult(f"heading:{heading}", heading in low, "template heading preserved"))
        results.append(CheckResult("no_tbd_placeholders", "[tbd" not in low and "[insert" not in low, "no leftover placeholders"))
        results.append(CheckResult("verified_root_cause", "connection pool" in low and "shard-03" in low, "verified root cause included"))
        results.append(CheckResult("sla_credit_10pct_95min", "10%" in low and "95" in low, "95 min outage and 10% SLA credit"))
        results.append(CheckResult("no_internal_blame_leak", all(w not in low for w in ("botched", "stupid", "dave")), "internal blame scrubbed"))

    if not actions.is_file():
        results.append(CheckResult("action_items_exists", False, "action_items.csv not found"))
    else:
        with actions.open("r", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        results.append(CheckResult("action_items_rows", len(rows) >= 3, f"found {len(rows)} action items"))
    return results
