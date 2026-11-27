import unittest

from helpdesk.rules import engine
from helpdesk.tickets import status
from tests.helpers import ADA, LEE, new_desk, ticket


class Mail(unittest.TestCase):
    def test_escalation_is_mailed(self):
        desk = new_desk()
        made = ticket(desk, priority="urgent")
        desk.clock.advance(minutes=30)
        engine.run(desk)
        mails = desk.outbox.to(LEE.email)
        self.assertEqual(len(mails), 1)
        self.assertEqual(mails[0].subject, f"[#{made.id}] Passed to Lee")

    def test_closing_is_mailed_to_the_requester(self):
        desk = new_desk()
        status.close(desk, ticket(desk))
        self.assertEqual(desk.outbox.to(ADA.email)[-1].subject, "[#1] Closed")
