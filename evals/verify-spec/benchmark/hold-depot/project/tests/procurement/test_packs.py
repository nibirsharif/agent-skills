import unittest

from depot.procurement import payload
from depot.procurement.packs import whole_packs
from depot.core.models import Order
from tests.helpers import ACME, BOLT


class Packs(unittest.TestCase):
    def test_units_are_rounded_up_to_whole_packs(self):
        self.assertEqual(whole_packs(50, 12), 5)
        self.assertEqual(whole_packs(48, 12), 4)
        self.assertEqual(whole_packs(1, 12), 1)

    def test_payload_names_the_order(self):
        self.assertEqual(payload.of(Order(7, BOLT, ACME, 24)), {"order": 7, "sku": BOLT, "units": 24})
