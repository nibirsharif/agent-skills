"""A depot with a set clock, one supplier, and one item, for the tests."""

import datetime
import decimal

from depot.app import Depot
from depot.core.clock import Clock
from depot.core.models import Item, Supplier

NOW = datetime.datetime(2026, 11, 23, 7, 0)
ACME = Supplier("Acme", "https://acme.example/orders")
BOLT = "BLT-0001"


def new_depot():
    return Depot(Clock(NOW))


def item(depot, sku=BOLT, stock=12, floor=10, batch=24, supplier=ACME, **more):
    return depot.store.put_item(Item(sku, "M6 bolt", supplier, stock, floor, batch, decimal.Decimal("0.10"), **more))
