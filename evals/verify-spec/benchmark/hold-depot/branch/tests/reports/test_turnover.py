import unittest

from depot.reports import turnover
from depot.stock import moves
from tests.helpers import BOLT, new_depot, item


class Turnover(unittest.TestCase):
    def test_picked_units_are_totalled_per_item(self):
        depot = new_depot()
        item(depot, stock=40, floor=0)
        item(depot, sku="NUT-0002", stock=40, floor=0)
        moves.pick(depot, BOLT, 5)
        moves.pick(depot, BOLT, 2)
        self.assertEqual(turnover.picked(depot), {BOLT: 7})
        self.assertEqual(turnover.slowest(depot), ["NUT-0002", BOLT])
