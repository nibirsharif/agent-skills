"""Amounts as text."""

import decimal


def show(amount, currency):
    return f"{decimal.Decimal(amount).quantize(decimal.Decimal('0.01'))} {currency}"
