class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = {}

    def allow(self, key: str, now: float) -> bool:
        hits = self._hits.setdefault(key, [])
        # BUG: keeps expired timestamps (now - t <= window instead of < window) and records denied attempts
        hits[:] = [t for t in hits if now - t <= self.window_seconds]
        hits.append(now)
        return len(hits) <= self.max_requests
