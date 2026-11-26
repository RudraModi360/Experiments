from app.auth import verify_token
def get_user(token, now=None):
    # BUG 2: uses <= for expiry indirectly via verify; also wrong method check
    if token is None or not token:
        return None
    return verify_token(token, now=now)
def list_items(token, now=None):
    user = get_user(token, now=now)
    if user is None:
        return 401, []
    return 200, [{"id":1}]
