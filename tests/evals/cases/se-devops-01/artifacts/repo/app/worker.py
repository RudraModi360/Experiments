import os
import sys
from pathlib import Path

READY_FILE = Path("/tmp/worker.ready")

def validate_env() -> None:
    missing = [k for k in ("REDIS_URL", "PAYMENT_SIGNING_KEY") if not os.environ.get(k)]
    if missing:
        raise KeyError(f"Missing required environment variables: {', '.join(missing)}")

def main() -> int:
    validate_env()
    if "--check" in sys.argv:
        print(f"worker ok redis={os.environ['REDIS_URL']} ready_path={READY_FILE}")
        return 0
    READY_FILE.write_text("ok\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
