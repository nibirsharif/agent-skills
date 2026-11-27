"""A purchase order as the supplier's endpoint takes it."""


def of(order):
    return {"order": order.id, "sku": order.sku, "units": order.qty}
