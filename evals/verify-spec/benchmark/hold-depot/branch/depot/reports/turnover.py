"""How fast stock moves: units picked per item over a number of days."""

import datetime


def picked(depot, days=30):
    since = depot.clock.now() - datetime.timedelta(days=days)
    totals = {}
    for move in depot.store.moves:
        if move.reason == "pick" and move.at >= since:
            totals[move.sku] = totals.get(move.sku, 0) - move.delta
    return totals


def slowest(depot, days=30):
    totals = picked(depot, days)
    return sorted((item.sku for item in depot.store.items()), key=lambda sku: totals.get(sku, 0))
