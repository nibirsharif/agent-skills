import decimal
import unittest

from depot.util import money, skus


class Util(unittest.TestCase):
    def test_money_has_two_places(self):
        self.assertEqual(money.show(decimal.Decimal("4"), "EUR"), "4.00 EUR")

    def test_good_sku_passes(self):
        self.assertEqual(skus.check("BLT-0001"), "BLT-0001")

    def test_bad_sku_is_refused(self):
        with self.assertRaises(skus.BadSku):
            skus.check("bolt-1")
