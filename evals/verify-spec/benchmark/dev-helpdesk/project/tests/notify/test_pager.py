import datetime
import unittest

from helpdesk.notify import digest
from helpdesk.rules import engine
from tests.helpers import LEE, MAX, NOW, new_desk, ticket


class Pages(unittest.TestCase):
    def test_unanswered_escalation_pages_the_manager(self):
        desk = new_desk()
        made = ticket(desk, priority="urgent")
        desk.clock.advance(minutes=30)
        engine.run(desk)
        desk.clock.advance(hours=2)
        desk.pager.page(made.team.on_call_manager, f"#{made.id} has waited 2 hours on the lead")
        self.assertEqual(desk.pager.pages, [(MAX.email, "#1 has waited 2 hours on the lead")])


class Digest(unittest.TestCase):
    def test_digest_goes_out_at_the_digest_hour(self):
        desk = new_desk()
        ticket(desk)
        ticket(desk)
        desk.clock.set(NOW.replace(hour=8) + datetime.timedelta(days=1))
        self.assertEqual(digest.send_digests(desk), 1)
        self.assertEqual(desk.outbox.to(LEE.email)[-1].subject, "2 open tickets")

    def test_no_digest_at_other_hours(self):
        desk = new_desk()
        ticket(desk)
        self.assertEqual(digest.send_digests(desk), 0)
