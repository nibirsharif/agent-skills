import datetime
import unittest
from unittest import mock

from mailing import tokens, web
from mailing.models import Subscriber
from mailing.service import SubscriptionService
from mailing.store import SubscriberStore

NOW = datetime.datetime(2026, 11, 21, 10, 0)


class Pages(unittest.TestCase):
    def setUp(self):
        self.service = SubscriptionService(SubscriberStore(), mock.Mock(), lambda: NOW)

    def test_subscribe_page_stores_the_address(self):
        self.assertEqual(web.handle(self.service, "/subscribe/ada@example.org")[0], 200)
        self.assertTrue(self.service.store.has("ada@example.org"))

    def test_subscribe_page_refuses_a_bad_address(self):
        self.assertEqual(web.handle(self.service, "/subscribe/ada")[0], 400)

    def test_confirm_page_activates(self):
        web.handle(self.service, "/subscribe/ada@example.org")
        status, _ = web.handle(self.service, "/confirm/" + tokens.make("ada@example.org"))
        self.assertEqual(status, 200)
        self.assertEqual(self.service.store.get("ada@example.org").status, "active")

    def test_unsubscribe_link_unsubscribes_the_address(self):
        self.service.store.add(Subscriber("ada@example.org", "active", NOW))
        status, text = web.unsubscribe_page(self.service, tokens.make("ada@example.org"))
        self.assertEqual((status, text), (200, "You are unsubscribed."))
        self.assertEqual(self.service.store.get("ada@example.org").status, "unsubscribed")

    def test_unknown_path_is_not_found(self):
        self.assertEqual(web.handle(self.service, "/archive/")[0], 404)
