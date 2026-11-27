"""Which handler answers which request."""

from depot.api import handlers

ROUTES = {
    ("POST", "/picks"): handlers.post_pick,
    ("POST", "/counts"): handlers.post_count,
    ("POST", "/orders"): handlers.post_order,
    ("POST", "/receipts"): handlers.post_receipt,
}


class NoRoute(Exception):
    pass


def dispatch(depot, method, path, **fields):
    try:
        handler = ROUTES[(method, path)]
    except KeyError:
        raise NoRoute(f"{method} {path}") from None
    return handler(depot, **fields)
