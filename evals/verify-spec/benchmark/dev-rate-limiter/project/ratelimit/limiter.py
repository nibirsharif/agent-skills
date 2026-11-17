"""A sliding-window request limiter."""

import time

LIMIT = 5
WINDOW_SECONDS = 60


class RateLimited(Exception):
    """Raised when a client is over the limit."""


class Limiter:
    def __init__(self, clock=time.monotonic):
        self._clock = clock
        self._seen = {}

    def check(self, client):
        """Record a request from client, or raise RateLimited when it is over the limit."""
        now = self._clock()
        recent = [t for t in self._seen.get(client, []) if now - t < WINDOW_SECONDS]
        if len(recent) >= LIMIT:
            self._seen[client] = recent
            raise RateLimited(f"{client} is over the limit")
        recent.append(now)
        self._seen[client] = recent
