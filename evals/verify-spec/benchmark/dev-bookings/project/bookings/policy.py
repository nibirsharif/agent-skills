"""What a cancellation costs."""

import decimal

LATE_HOURS = 24
LATE_FEE = decimal.Decimal("0.20")


def is_late(hours_before_start):
    """Whether a cancellation this many hours before the start is a late one."""
    return hours_before_start < LATE_HOURS


def refund_for(price, late):
    """The amount to give back: the price, less the late fee for a late cancellation."""
    if not late:
        return price
    return (price - price * LATE_FEE).quantize(decimal.Decimal("0.01"))
