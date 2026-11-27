"""Goods arriving at the dock."""

from depot.stock.moves import move


class NotSent(Exception):
    pass


def receive(depot, order_id, qty=None):
    order = depot.store.order(order_id)
    if order.status != "sent":
        raise NotSent(order_id)
    order.status = "received"
    order.received_at = depot.clock.now()
    move(depot, order.sku, order.qty if qty is None else qty, "receipt")
    return order
