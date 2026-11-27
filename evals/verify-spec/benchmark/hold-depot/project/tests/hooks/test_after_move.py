import unittest

from depot.stock import moves
from tests.helpers import BOLT, new_depot, item


class Replenish(unittest.TestCase):
    def setUp(self):
        self.depot = new_depot()

    def test_stock_falling_below_the_floor_drafts_an_order(self):
        item(self.depot, stock=12, floor=10)
        moves.pick(self.depot, BOLT, 3)
        orders = self.depot.store.orders(BOLT)
        self.assertEqual(len(orders), 1)
        self.assertEqual((orders[0].sku, orders[0].status), (BOLT, "draft"))

    def test_stock_at_the_floor_drafts_nothing(self):
        item(self.depot, stock=12, floor=10)
        moves.pick(self.depot, BOLT, 2)
        self.assertEqual(self.depot.store.orders(BOLT), [])

    def test_order_is_for_the_batch(self):
        item(self.depot, stock=12, floor=10, batch=24)
        moves.pick(self.depot, BOLT, 3)
        self.assertEqual(self.depot.store.orders(BOLT)[0].qty, 24)

    def test_item_with_an_order_waiting_gets_no_second_one(self):
        item(self.depot, stock=12, floor=10)
        moves.pick(self.depot, BOLT, 3)
        moves.move(self.depot, BOLT, 5, "count")
        moves.pick(self.depot, BOLT, 6)
        self.assertEqual(len(self.depot.store.orders(BOLT)), 1)
        self.depot.store.orders(BOLT)[0].status = "sent"
        moves.move(self.depot, BOLT, 5, "count")
        moves.pick(self.depot, BOLT, 6)
        self.assertEqual(len(self.depot.store.orders(BOLT)), 1)

    def test_received_order_lets_the_next_one_through(self):
        item(self.depot, stock=12, floor=10)
        moves.pick(self.depot, BOLT, 3)
        self.depot.store.orders(BOLT)[0].status = "received"
        moves.move(self.depot, BOLT, 5, "count")
        moves.pick(self.depot, BOLT, 6)
        self.assertEqual(len(self.depot.store.orders(BOLT)), 2)

    def test_discontinued_item_is_not_ordered(self):
        item(self.depot, stock=12, floor=10, discontinued=True)
        moves.pick(self.depot, BOLT, 3)
        self.assertEqual(self.depot.store.orders(BOLT), [])
