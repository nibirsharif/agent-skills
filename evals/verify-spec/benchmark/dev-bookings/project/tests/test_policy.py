import decimal
import unittest

from bookings import policy


class Late(unittest.TestCase):
    def test_under_24_hours_is_late(self):
        self.assertTrue(policy.is_late(23))

    def test_24_hours_is_not_late(self):
        self.assertFalse(policy.is_late(24))


class Refund(unittest.TestCase):
    def test_late_refund_keeps_20_percent(self):
        self.assertEqual(policy.refund_for(decimal.Decimal("100.00"), late=True), decimal.Decimal("80.00"))

    def test_early_refund_is_the_price(self):
        self.assertEqual(policy.refund_for(decimal.Decimal("100.00"), late=False), decimal.Decimal("100.00"))
