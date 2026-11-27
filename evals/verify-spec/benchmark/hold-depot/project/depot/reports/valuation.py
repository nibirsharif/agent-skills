"""What the stock is worth."""

from depot import settings
from depot.util.money import show


def total(depot):
    return sum(item.stock * item.unit_cost for item in depot.store.items())


def line(depot):
    return f"Stock value: {show(total(depot), settings.CURRENCY)}"
