from __future__ import annotations
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def check(ctx):
    xlsx = ctx.workspace.root / "FY26_Operating_Model.xlsx"
    if not xlsx.is_file():
        return [CheckResult("xlsx_exists", False, "FY26_Operating_Model.xlsx not found")]
    results = []
    try:
        with zipfile.ZipFile(xlsx, "r") as zf:
            wb_xml = zf.read("xl/workbook.xml").decode("utf-8", "replace")
            sheet_names = [
                el.attrib.get("name", "")
                for el in ET.fromstring(wb_xml).iter()
                if el.tag.endswith("}sheet") or el.tag == "sheet"
            ]
            low_names = {s.lower() for s in sheet_names}
            results.append(CheckResult("has_required_tabs", len(sheet_names) >= 3 and any("summary" in s for s in low_names), f"tabs={sheet_names}"))
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
            results.append(CheckResult("live_formulas_present", len(formulas) >= 5, f"found {len(formulas)} formulas"))
            has_errors = any(err in all_xml for err in ("#REF!", "#VALUE!", "#DIV/0!", "#NAME?"))
            results.append(CheckResult("zero_formula_errors", not has_errors, "checked for Excel error tokens"))
            out_low = (ctx.final_output + " " + all_xml).lower()
            results.append(CheckResult("reconciled_rev_820k", "820,000" in out_low or "820000" in out_low, "checks $820,000 consolidated revenue"))
            results.append(CheckResult("reconciled_opex_497k", "497,000" in out_low or "497000" in out_low, "checks $497,000 adjusted OpEx"))
    except Exception as exc:
        results.append(CheckResult("valid_xlsx_zip", False, str(exc)))
    return results
