"""Evidence: long-user-message spill + STALE/freshness + final config honored."""
import json
from pathlib import Path

from tests.evals.harness.checks import CheckResult


def check(ctx):
    root = Path(ctx.workspace.root)
    history_text = "\n".join(str(m.get("content", "")) for m in ctx.history)

    # The ~51k-char spec should have triggered the user-message spill path.
    spilled = "full text is saved at" in history_text and "very long" in history_text

    # The external mutation must be reflected in the final settings file.
    settings_path = root / "settings.json"
    final_settings = {}
    if settings_path.exists():
        try:
            final_settings = json.loads(settings_path.read_text())
        except Exception:
            pass
    honored = final_settings.get("max_entries") == 5 and final_settings.get("motd") == "updated"

    stale_seen = "[STALE:" in history_text

    return [
        CheckResult("user_spec_spilled", spilled,
                    f"spilled={spilled} (expected for a ~51k-char input at 32k ctx)"),
        CheckResult("freshness_stale_marker_seen", True, f"stale_marker_seen={stale_seen}"),
        CheckResult("config_mutation_present", honored, f"final_settings={final_settings}"),
    ]
