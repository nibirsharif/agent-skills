"""The buyer's list of orders that are overdue."""


def overdue_orders(depot):
    return [order for order in depot.store.orders() if order.overdue]


def lines(depot):
    return [f"#{o.id} {o.sku} from {o.supplier.name}, sent {o.sent_at:%Y-%m-%d}" for o in overdue_orders(depot)]
