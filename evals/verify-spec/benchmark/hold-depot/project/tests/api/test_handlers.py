import unittest

from depot.api import handlers, router
from depot.core.models import Order
from tests.helpers import ACME, BOLT, NOW, new_depot, item


class Requests(unittest.TestCase):
    def setUp(self):
        self.depot = new_depot()
        self.item = item(self.depot, stock=40, floor=10)

    def test_pick_request_takes_stock(self):
        router.dispatch(self.depot, "POST", "/picks", sku=BOLT, qty=4)
        self.assertEqual(self.item.stock, 36)

    def test_count_request_corrects_stock(self):
        self.assertEqual(router.dispatch(self.depot, "POST", "/counts", sku=BOLT, counted=30), -10)

    def test_order_request_drafts_an_order(self):
        order = router.dispatch(self.depot, "POST", "/orders", sku=BOLT)
        self.assertEqual((order.sku, order.status), (BOLT, "draft"))

    def test_second_order_request_is_refused(self):
        router.dispatch(self.depot, "POST", "/orders", sku=BOLT)
        with self.assertRaises(handlers.Refused):
            router.dispatch(self.depot, "POST", "/orders", sku=BOLT)

    def test_receipt_request_receives_the_order(self):
        self.depot.store.put_order(Order(1, BOLT, ACME, 24, "sent", NOW))
        self.assertEqual(router.dispatch(self.depot, "POST", "/receipts", order_id=1).status, "received")

    def test_unknown_request_has_no_route(self):
        with self.assertRaises(router.NoRoute):
            router.dispatch(self.depot, "GET", "/nothing")
