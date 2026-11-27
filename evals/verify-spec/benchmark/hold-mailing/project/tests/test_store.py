import datetime
import unittest

from mailing.models import Subscriber
from mailing.store import SubscriberStore

NOW = datetime.datetime(2026, 11, 21, 10, 0)


class Active(unittest.TestCase):
    def test_active_leaves_out_unsubscribed_and_bounced(self):
        store = SubscriberStore()
        store.add(Subscriber("ada@example.org", "active", NOW))
        store.add(Subscriber("bo@example.org", "unsubscribed", NOW))
        store.add(Subscriber("cy@example.org", "bounced", NOW))
        self.assertEqual([s.address for s in store.active()], ["ada@example.org"])

    def test_set_status_changes_the_subscriber(self):
        store = SubscriberStore()
        store.add(Subscriber("ada@example.org", "pending", NOW))
        store.set_status("ada@example.org", "active")
        self.assertEqual(store.get("ada@example.org").status, "active")
