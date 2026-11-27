"""Drafting purchase orders."""

from depot.core.models import Order
from depot.procurement.packs import whole_packs

WAITING = ("draft", "sent")


def open_for(depot, item):
    """A draft order for the item, or None when one is already on its way."""
    if any(order.status in WAITING for order in depot.store.orders(item.sku)):
        return None
    qty = whole_packs(item.batch, item.supplier.pack_size)
    return depot.store.put_order(Order(depot.store.next_order_id(), item.sku, item.supplier, qty))
