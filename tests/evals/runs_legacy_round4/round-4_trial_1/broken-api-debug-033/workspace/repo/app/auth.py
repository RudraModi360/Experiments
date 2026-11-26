"""Auth."""
import base64, hashlib, hmac, json, time
SECRET=b"key"
def _sign(p): return hmac.new(SECRET,p.encode(),hashlib.sha256).hexdigest()
def issue_token(user,ttl=60,now=None):
    now=time.time() if now is None else now
    payload=base64.urlsafe_b64encode(json.dumps({"user":user,"exp":now+ttl}).encode()).decode()
    return payload+"."+_sign(payload)
def verify_token(token,now=None):
    now=time.time() if now is None else now
    try:
        payload,sig=token.split(".")
        if not hmac.compare_digest(sig,_sign(payload)): return None
        data=json.loads(base64.urlsafe_b64decode(payload.encode()))
        if data["exp"] < now:  # Fixed boundary: token should be valid at exp time (now == exp)
            return None
        return data["user"]
    except Exception:
        return None
