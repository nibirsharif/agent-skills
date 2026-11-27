"""Goods going back to a supplier."""

import datetime

from depot import settings
from depot.stock.moves import move


class TooLate(Exception):
    pass


def send_back(depot, order_id, qty):
    order = depot.store.order(order_id)
    if depot.clock.now() - order.received_at > datetime.timedelta(days=settings.RETURN_WINDOW_DAYS):
        raise TooLate(order_id)
    move(depot, order.sku, -qty, "return")
    return order
