"""What each request does. A handler takes the depot and the request's fields."""

from depot.procurement import drafts
from depot.receiving import dock
from depot.stock import counts, moves


class Refused(Exception):
    pass


def post_pick(depot, sku, qty):
    return moves.pick(depot, sku, qty)


def post_count(depot, sku, counted):
    return counts.record_count(depot, sku, counted)


def post_order(depot, sku):
    """The buyer orders an item by hand, whatever its stock."""
    order = drafts.open_for(depot, depot.store.item(sku))
    if order is None:
        raise Refused(f"{sku} already has an order on its way")
    return order


def post_receipt(depot, order_id, qty=None):
    return dock.receive(depot, order_id, qty)
