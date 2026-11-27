import datetime
import unittest
from unittest import mock

from mailing import tokens
from mailing.addresses import InvalidAddress
from mailing.models import Subscriber
from mailing.service import AlreadySubscribed, SubscriptionService
from mailing.store import SubscriberStore

NOW = datetime.datetime(2026, 11, 21, 10, 0)


def new_service():
    return SubscriptionService(SubscriberStore(), mock.Mock(), lambda: NOW)


class Subscribe(unittest.TestCase):
    def setUp(self):
        self.service = new_service()

    def test_new_address_is_stored_pending(self):
        self.service.subscribe("ada@example.org")
        self.assertEqual(self.service.store.get("ada@example.org").status, "pending")

    def test_address_without_at_is_rejected(self):
        with self.assertRaises(InvalidAddress):
            self.service.subscribe("ada.example.org")
        self.assertEqual(self.service.store.count(), 0)

    def test_address_already_stored_is_rejected(self):
        self.service.subscribe("ada@example.org")
        with self.assertRaises(AlreadySubscribed):
            self.service.subscribe("ada@example.org")
        self.assertEqual(self.service.store.count(), 1)

    def test_confirmation_link_is_mailed(self):
        self.service.subscribe("ada@example.org")
        to, subject, body = self.service.mailer.send.call_args.args
        self.assertEqual(to, "ada@example.org")
        self.assertEqual(body, "/confirm/" + tokens.make("ada@example.org"))


class Confirm(unittest.TestCase):
    def test_confirmation_makes_the_subscriber_active(self):
        service = new_service()
        service.subscribe("ada@example.org")
        service.confirm(tokens.make("ada@example.org"))
        self.assertEqual(service.store.get("ada@example.org").status, "active")


class Unsubscribe(unittest.TestCase):
    def setUp(self):
        self.service = new_service()
        self.service.store.add(Subscriber("ada@example.org", "active", NOW))

    def test_unsubscribe_sets_the_status(self):
        self.service.unsubscribe("ada@example.org")
        self.assertEqual(self.service.store.get("ada@example.org").status, "unsubscribed")

    def test_unsubscribe_sends_one_confirmation(self):
        self.service.unsubscribe("ada@example.org")
        self.service.mailer.send.assert_called_once_with("ada@example.org", "You are unsubscribed", mock.ANY)
