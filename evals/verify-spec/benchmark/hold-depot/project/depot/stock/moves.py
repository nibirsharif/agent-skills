"""Stock going in and out. Every change to an item's stock is a movement."""

from depot.core.models import Move


class NotEnoughStock(Exception):
    pass


def move(depot, sku, delta, reason):
    item = depot.store.item(sku)
    if item.stock + delta < 0:
        raise NotEnoughStock(sku)
    before = item.stock
    item.stock += delta
    depot.store.moves.append(Move(sku, delta, reason, depot.clock.now()))
    depot.bus.publish("stock.moved", depot=depot, item=item, before=before)
    return item


def pick(depot, sku, qty):
    return move(depot, sku, -qty, "pick")
