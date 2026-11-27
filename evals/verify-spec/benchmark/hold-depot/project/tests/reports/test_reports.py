import unittest
from unittest import mock

from depot.core.models import Order
from depot.jobs import nightly
from depot.reports import overdue, valuation
from tests.helpers import ACME, BOLT, NOW, new_depot, item


class Reports(unittest.TestCase):
    def setUp(self):
        self.depot = new_depot()
        item(self.depot, stock=40, floor=0)

    def test_stock_value(self):
        self.assertEqual(valuation.line(self.depot), "Stock value: 4.00 EUR")

    def test_overdue_orders_are_listed(self):
        order = self.depot.store.put_order(Order(1, BOLT, ACME, 24, "sent", NOW))
        self.depot.clock.advance(days=15)
        order.overdue = True
        self.assertEqual(overdue.lines(self.depot), ["#1 BLT-0001 from Acme, sent 2026-11-23"])

    def test_order_that_is_not_overdue_is_left_out(self):
        self.depot.store.put_order(Order(1, BOLT, ACME, 24, "sent", NOW))
        self.assertEqual(overdue.lines(self.depot), [])

    def test_nightly_run_reports_what_it_sent(self):
        self.depot.store.put_order(Order(1, BOLT, ACME, 24))
        self.assertEqual(nightly.run(self.depot, mock.Mock())[0], "1 orders sent")
