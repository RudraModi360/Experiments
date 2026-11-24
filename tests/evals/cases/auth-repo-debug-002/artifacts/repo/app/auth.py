"""Token issue/verify."""
import base64, hashlib, hmac, json, time
SECRET = b"eval-secret-key"
def _sign(payload): return hmac.new(SECRET, payload.encode(), hashlib.sha256).hexdigest()
def issue_token(user, ttl=60, now=None):
    now = time.time() if now is None else now
    payload = base64.urlsafe_b64encode(json.dumps({"user": user, "exp": now + ttl}).encode()).decode()
    return payload + "." + _sign(payload)
def verify_token(token, now=None):
    now = time.time() if now is None else now
    try:
        payload, sig = token.split(".")
        if not hmac.compare_digest(sig, _sign(payload)): return None
        data = json.loads(base64.urlsafe_b64decode(payload.encode()))
        if data["exp"] <= now:  # BUG
            return None
        return data["user"]
    except Exception:
        return None
