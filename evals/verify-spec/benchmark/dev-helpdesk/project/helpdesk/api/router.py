"""Which handler answers which request."""

from helpdesk.api import handlers

ROUTES = {
    ("GET", "/queue"): handlers.queue,
    ("POST", "/tickets"): handlers.post_ticket,
    ("POST", "/tickets/reply"): handlers.post_reply,
    ("POST", "/tickets/close"): handlers.post_close,
    ("POST", "/tickets/handoff"): handlers.post_handoff,
}


class NoRoute(Exception):
    pass


def dispatch(desk, method, path, user, **fields):
    try:
        handler = ROUTES[(method, path)]
    except KeyError:
        raise NoRoute(f"{method} {path}") from None
    return handler(desk, user, **fields)
