import datetime
import time
import unittest
from unittest import mock

from mailing import report
from mailing.campaigns import Campaigns, SendResult
from mailing.models import Subscriber
from mailing.store import SubscriberStore

NOW = datetime.datetime(2026, 11, 21, 10, 0)


class Send(unittest.TestCase):
    def test_campaign_goes_to_active_subscribers_only(self):
        store, mailer = mock.Mock(), mock.Mock()
        store.active.return_value = [Subscriber("ada@example.org", "active", NOW)]
        result = Campaigns(store, mailer).send("Hello", "News")
        mailer.send.assert_called_once_with("ada@example.org", "Hello", "News")
        self.assertEqual(result.sent, 1)

    def test_refused_message_is_reported_bounced(self):
        campaigns = Campaigns(SubscriberStore(), mock.Mock())
        refused = SendResult(sent=1, bounced=["bo@example.org"])
        with mock.patch.object(Campaigns, "send", return_value=refused):
            text = report.after_send(campaigns, "Hello", "News")
        self.assertEqual(text, "Hello: 1 sent\n1 bounced: bo@example.org\n")

    def test_report_without_bounces_is_one_line(self):
        store = SubscriberStore()
        store.add(Subscriber("ada@example.org", "active", NOW))
        self.assertEqual(report.after_send(Campaigns(store, mock.Mock()), "Hello", "News"), "Hello: 1 sent\n")


class Speed(unittest.TestCase):
    def test_recipient_list_is_built_quickly(self):
        store = SubscriberStore()
        for n in range(500):
            store.add(Subscriber(f"reader{n}@example.org", "active", NOW))
        started = time.perf_counter()
        recipients = Campaigns(store, mock.Mock()).recipients()
        self.assertLess(time.perf_counter() - started, 1.0)
        self.assertEqual(len(recipients), 500)
