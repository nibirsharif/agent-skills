import unittest

from depot.core.models import Order
from depot.receiving import dock, returns
from tests.helpers import ACME, BOLT, NOW, new_depot, item


class Receiving(unittest.TestCase):
    def setUp(self):
        self.depot = new_depot()
        item(self.depot, stock=9, floor=10)
        self.order = self.depot.store.put_order(Order(1, BOLT, ACME, 24, "sent", NOW))

    def test_received_order_is_marked_received(self):
        self.depot.clock.advance(days=3)
        dock.receive(self.depot, 1)
        self.assertEqual(self.order.status, "received")
        self.assertEqual(self.order.received_at, self.depot.clock.now())

    def test_order_that_was_not_sent_is_refused(self):
        self.order.status = "draft"
        with self.assertRaises(dock.NotSent):
            dock.receive(self.depot, 1)

    def test_return_after_the_window_is_refused(self):
        dock.receive(self.depot, 1)
        self.depot.clock.advance(days=31)
        with self.assertRaises(returns.TooLate):
            returns.send_back(self.depot, 1, 4)

    def test_return_inside_the_window_is_a_movement(self):
        dock.receive(self.depot, 1)
        returns.send_back(self.depot, 1, 4)
        self.assertEqual(self.depot.store.moves[-1].reason, "return")
