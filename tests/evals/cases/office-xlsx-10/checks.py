from __future__ import annotations
import xml.etree.ElementTree as ET
import zipfile
from tests.evals.harness.checks import CheckResult


def check(ctx):
    xlsx = ctx.workspace.root / "Team_Offsite_Plan.xlsx"
    if not xlsx.is_file():
        return [CheckResult("xlsx_exists", False, "Team_Offsite_Plan.xlsx not found")]
    with zipfile.ZipFile(xlsx, "r") as zf:
        wb_xml = zf.read("xl/workbook.xml").decode("utf-8", "replace")
        sheets = [
            el.attrib.get("name", "")
            for el in ET.fromstring(wb_xml).iter()
            if el.tag.endswith("}sheet") or el.tag == "sheet"
        ]
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
        CheckResult("multi_sheet_xlsx", len(sheets) >= 2, f"sheets={sheets}"),
        CheckResult("live_formulas", len(formulas) >= 2, f"found {len(formulas)} formulas"),
        CheckResult("headcount_20", "20" in combined, "deduped active headcount 20"),
        CheckResult("total_5900_and_variance_600", ("5,900" in combined or "5900" in combined) and "600" in combined, "total $5,900 and $600 under budget"),
    ]
