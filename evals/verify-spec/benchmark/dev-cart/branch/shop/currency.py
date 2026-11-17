"""Show an amount in another currency."""

from decimal import Decimal

RATES = {"EUR": Decimal("1"), "USD": Decimal("1.08"), "GBP": Decimal("0.86")}


def convert(amount, currency):
    return (amount * RATES[currency]).quantize(Decimal("0.01"))
