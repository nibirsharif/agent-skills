import unittest

from depot.stock import counts, locations, moves, reorder
from tests.helpers import BOLT, new_depot, item


class Moves(unittest.TestCase):
    def setUp(self):
        self.depot = new_depot()
        self.item = item(self.depot, stock=40, floor=0)

    def test_pick_takes_stock(self):
        moves.pick(self.depot, BOLT, 5)
        self.assertEqual(self.item.stock, 35)
        self.assertEqual(self.depot.store.moves[-1].reason, "pick")

    def test_pick_of_more_than_the_stock_is_refused(self):
        with self.assertRaises(moves.NotEnoughStock):
            moves.pick(self.depot, BOLT, 41)
        self.assertEqual(self.item.stock, 40)

    def test_count_within_the_tolerance_changes_nothing(self):
        self.assertEqual(counts.record_count(self.depot, BOLT, 38), 0)
        self.assertEqual(self.item.stock, 40)

    def test_count_outside_the_tolerance_corrects_the_stock(self):
        self.assertEqual(counts.record_count(self.depot, BOLT, 30), -10)
        self.assertEqual(self.item.stock, 30)


class Planning(unittest.TestCase):
    def test_suggested_point_covers_lead_time_and_safety(self):
        self.assertEqual(reorder.suggest_point(daily_use=4, lead_days=7), 40)
        self.assertEqual(reorder.suggest_quantity(daily_use=4), 120)

    def test_days_of_cover(self):
        depot = new_depot()
        self.assertEqual(reorder.days_of_cover(item(depot, stock=40), daily_use=8), 5)


class Locations(unittest.TestCase):
    def test_shelve_and_find_by_aisle(self):
        depot = new_depot()
        item(depot)
        locations.shelve(depot, BOLT, "a-3-2")
        self.assertEqual([i.location for i in locations.in_aisle(depot, "A")], ["A-03-2"])

    def test_bad_location_is_refused(self):
        with self.assertRaises(locations.BadLocation):
            locations.parse("A3")
