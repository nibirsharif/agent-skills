"""Suggested reorder points, for the buyer's planning page. Nothing here orders anything."""


def suggest_point(daily_use, lead_days, safety_days=3):
    """A reorder point that covers the supplier's lead time and a few days more."""
    return daily_use * (lead_days + safety_days)


def suggest_quantity(daily_use, cover_days=30):
    return daily_use * cover_days


def days_of_cover(item, daily_use):
    return item.stock // daily_use if daily_use else None
