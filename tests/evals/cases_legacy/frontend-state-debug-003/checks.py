"""Evidence: save and load must reference the same storage key."""
import re
from pathlib import Path

from tests.evals.harness.checks import CheckResult


def check(ctx):
    app = Path(ctx.workspace.root) / "site" / "app.js"
    text = app.read_text(encoding="utf-8") if app.exists() else ""
    save = re.search(r'SAVE_KEY\s*=\s*["\']([^"\']+)["\']', text)
    load = re.search(r'LOAD_KEY\s*=\s*["\']([^"\']+)["\']', text)
    if load is None:
        ok, detail = True, "LOAD_KEY removed; single shared key"
    elif save and save.group(1) == load.group(1):
        ok, detail = True, f"keys match: {save.group(1)}"
    else:
        ok = False
        detail = f"SAVE_KEY={save.group(1) if save else '?'} LOAD_KEY={load.group(1)}"
    return [CheckResult("storage_key_consistent", ok, detail)]
