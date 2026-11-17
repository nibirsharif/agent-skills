"""A shopping cart."""

from decimal import Decimal


class Cart:
    def __init__(self):
        self.items = []

    def add(self, name, price, quantity=1):
        self.items.append((name, Decimal(price), quantity))
