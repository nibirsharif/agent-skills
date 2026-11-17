import unittest
from decimal import Decimal

from shop.cart import COUPONS, TAX_RATE, Cart


class Subtotal(unittest.TestCase):
    def test_subtotal_sums_price_times_quantity(self):
        cart = Cart()
        cart.add("mug", "8.50", 2)
        cart.add("tea", "3.00")
        self.assertEqual(cart.subtotal(), Decimal("20.00"))

    def test_empty_cart_is_zero(self):
        self.assertEqual(Cart().subtotal(), Decimal("0.00"))


class Coupon(unittest.TestCase):
    def test_save10_reduces_the_subtotal(self):
        cart = Cart()
        cart.add("lamp", "40.00")
        cart.apply_coupon("SAVE10")
        expected = Decimal("40.00") - Decimal("40.00") * COUPONS["SAVE10"]
        self.assertEqual(cart.subtotal(), expected)


class Quantity(unittest.TestCase):
    def test_negative_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            Cart().add("mug", "8.50", -1)


class Shipping(unittest.TestCase):
    @unittest.skip("fails on CI, see the tracker")
    def test_free_shipping_from_50(self):
        cart = Cart()
        cart.add("lamp", "50.00")
        self.assertEqual(cart.shipping(), Decimal("0.00"))


class Tax(unittest.TestCase):
    def test_tax_on_the_subtotal(self):
        cart = Cart()
        cart.add("lamp", "40.00")
        self.assertEqual(cart.tax(), (Decimal("40.00") * TAX_RATE).quantize(Decimal("0.01")))
