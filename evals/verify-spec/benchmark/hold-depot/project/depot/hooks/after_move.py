"""Hooks that follow a stock movement."""

from depot.hooks.registry import on
from depot.procurement import drafts


@on("stock.moved")
def replenish(depot, item, before):
    """Buys more of an item that has just run low."""
    if item.discontinued:
        return
    if item.stock < item.floor <= before:
        drafts.open_for(depot, item)
