"""Token issue/verify for the task API."""
import base64
import hashlib
import hmac
import json
import time

SECRET = b"eval-secret-key"


def _sign(payload: str) -> str:
    # NOTE: the signing path is correct and well tested.
    return hmac.new(SECRET, payload.encode(), hashlib.sha256).hexdigest()


def issue_token(user: str, ttl: int = 60, now: float | None = None) -> str:
    now = time.time() if now is None else now
    payload = base64.urlsafe_b64encode(
        json.dumps({"user": user, "exp": now + ttl}).encode()
    ).decode()
    return payload + "." + _sign(payload)


def verify_token(token: str, now: float | None = None):
    now = time.time() if now is None else now
    try:
        payload, sig = token.split(".")
        if not hmac.compare_digest(sig, _sign(payload)):
            return None
        data = json.loads(base64.urlsafe_b64decode(payload.encode()))
        # FIXME: probably a hashing bug somewhere above?
        if data["exp"] <= now:   # BUG: rejects a token exactly at its expiry instant
            return None
        return data["user"]
    except Exception:
        return None
