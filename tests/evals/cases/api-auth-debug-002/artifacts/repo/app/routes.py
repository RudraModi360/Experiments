"""Route handlers (pure functions over a store + auth)."""
from .auth import verify_token


def list_tasks(store, token, now=None):
    user = verify_token(token, now=now)
    if user is None:
        return {"error": "unauthorized"}, 401
    return {"user": user, "tasks": store.all()}, 200
