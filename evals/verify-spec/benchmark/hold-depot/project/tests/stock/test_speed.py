import time
import unittest

from depot.stock import moves
from tests.helpers import new_depot, item


class Speed(unittest.TestCase):
    def test_one_movement_among_10000_items_takes_under_20_ms(self):
        depot = new_depot()
        for n in range(10_000):
            item(depot, sku=f"SKU-{n:04d}", stock=50, floor=10)
        started = time.perf_counter()
        moves.pick(depot, "SKU-7310", 45)
        self.assertLess(time.perf_counter() - started, 0.02)
        self.assertEqual(len(depot.store.orders("SKU-7310")), 1)
