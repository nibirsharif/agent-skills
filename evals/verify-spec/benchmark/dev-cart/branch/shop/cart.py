"""A shopping cart and its totals."""

from decimal import Decimal

COUPONS = {"SAVE10": Decimal("0.15")}
FREE_SHIPPING_FROM = Decimal("50.00")
SHIPPING = Decimal("4.99")
TAX_RATE = Decimal("0.20")


class Cart:
    def __init__(self):
        self.items = []
        self.coupon = None

    def add(self, name, price, quantity=1):
        if quantity < 0:
            raise ValueError("quantity must be at least 1")
        self.items.append((name, Decimal(price), quantity))

    def apply_coupon(self, code):
        if code not in COUPONS:
            raise KeyError(code)
        self.coupon = code

    def subtotal(self):
        total = sum((price * quantity for _, price, quantity in self.items), Decimal("0"))
        if self.coupon:
            total -= total * COUPONS[self.coupon]
        return total.quantize(Decimal("0.01"))

    def shipping(self):
        return Decimal("0.00") if self.subtotal() >= FREE_SHIPPING_FROM else SHIPPING

    def tax(self):
        return (self.subtotal() * TAX_RATE).quantize(Decimal("0.01"))
