from __future__ import annotations
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def check(ctx):
    xlsx = ctx.workspace.root / "Tax_Prep_2026.xlsx"
    if not xlsx.is_file():
        return [CheckResult("xlsx_exists", False, "Tax_Prep_2026.xlsx not found")]
    with zipfile.ZipFile(xlsx, "r") as zf:
        formulas = []
        all_xml = ""
        for name in zf.namelist():
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
                raw = zf.read(name).decode("utf-8", "replace")
                all_xml += " " + raw
                for el in ET.fromstring(raw).iter():
                    if el.tag.endswith("}f") or el.tag == "f":
                        if el.text:
                            formulas.append(el.text)
    combined = (ctx.final_output + " " + all_xml).lower()
    return [
        CheckResult("live_formulas", len(formulas) >= 3, f"found {len(formulas)} formulas"),
        CheckResult("no_formula_errors", not any(e in all_xml for e in ("#REF!", "#VALUE!", "#DIV/0!")), "clean formulas"),
        CheckResult("deductible_total_1909", "1,909" in combined or "1909" in combined, "checks $1,909 total deductible"),
        CheckResult("duplicate_and_transfer_noted", "duplicate" in combined and ("transfer" in combined or "autopay" in combined), "flags duplicate & transfer exclusion"),
    ]
