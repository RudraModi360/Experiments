"""Evidence: shared contract values across app.py / Dockerfile / compose.yaml."""
import re
from pathlib import Path

from tests.evals.harness.checks import CheckResult


def check(ctx):
    root = Path(ctx.workspace.root)

    def read(rel):
        p = root / rel
        return p.read_text(encoding="utf-8") if p.exists() else ""

    app = read("service/app.py")
    dockerfile = read("Dockerfile")
    compose = read("compose.yaml")

    expose = re.findall(r"EXPOSE\s+(\d+)", dockerfile)
    ports = re.findall(r"(\d+):\d+", compose)
    app_uses_port_env = "PORT" in app
    app_uses_token_env = "APP_TOKEN" in app
    compose_token = "demo-token-123" in compose
    multi_stage = dockerfile.count("FROM ") >= 2

    detail = (f"EXPOSE={expose} compose_ports={ports} app_PORT_env={app_uses_port_env} "
              f"app_APP_TOKEN_env={app_uses_token_env} compose_token={compose_token} "
              f"multi_stage={multi_stage}")
    ok = app_uses_port_env and app_uses_token_env and compose_token and multi_stage
    return [CheckResult("cross_file_contract_values", ok, detail)]
