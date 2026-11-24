from auth import verify_token
def list_tasks(token, now=None):
    if verify_token(token, now=now) is None:
        return 401, []
    return 200, []
