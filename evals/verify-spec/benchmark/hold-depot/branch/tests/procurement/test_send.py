import unittest
from unittest import mock

from depot.core.models import Order
from depot.procurement import send
from tests.helpers import ACME, BOLT, new_depot


class Send(unittest.TestCase):
    def setUp(self):
        self.depot = new_depot()
        self.order = self.depot.store.put_order(Order(1, BOLT, ACME, 24))
        self.transport = mock.Mock()

    def test_order_is_posted_to_the_suppliers_endpoint(self):
        send.send(self.depot, self.order, self.transport)
        self.transport.post.assert_called_once_with(
            "https://acme.example/orders", {"order": 1, "sku": BOLT, "units": 24})
        self.assertEqual((self.order.status, self.order.sent_at), ("sent", self.depot.clock.now()))

    def test_rejected_order_keeps_the_suppliers_reason(self):
        self.transport.post.side_effect = send.TransportError("unknown sku")
        with self.assertRaises(send.TransportError):
            send.send(self.depot, self.order, self.transport)
        self.assertEqual(self.order.note, "unknown sku")
        self.assertIsNone(self.order.sent_at)

    def test_send_drafts_skips_orders_already_sent(self):
        self.order.status = "sent"
        self.assertEqual(send.send_drafts(self.depot, self.transport), [])
        self.transport.post.assert_not_called()
