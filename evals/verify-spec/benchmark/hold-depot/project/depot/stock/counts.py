"""Stock takes: what was counted on the shelf against what the records say."""

from depot import settings
from depot.stock.moves import move


def record_count(depot, sku, counted):
    """Corrects the stock to the count when they differ by more than the tolerance. Returns the correction."""
    difference = counted - depot.store.item(sku).stock
    if abs(difference) <= settings.COUNT_TOLERANCE:
        return 0
    move(depot, sku, difference, "count")
    return difference
