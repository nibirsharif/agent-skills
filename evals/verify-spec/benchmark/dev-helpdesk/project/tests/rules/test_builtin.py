import unittest

from helpdesk.rules import engine
from helpdesk.tickets import status
from helpdesk.tickets.replies import add_reply
from tests.helpers import ADA, BO, LEE, new_desk, ticket


class StaleUrgent(unittest.TestCase):
    def setUp(self):
        self.desk = new_desk()
        self.ticket = ticket(self.desk, priority="urgent")

    def test_urgent_ticket_goes_to_the_lead_after_30_minutes(self):
        self.desk.clock.advance(minutes=29)
        self.assertEqual(engine.run(self.desk), [])
        self.assertIsNone(self.ticket.assignee)
        self.desk.clock.advance(minutes=1)
        self.assertEqual(engine.run(self.desk), [("stale-urgent", self.ticket.id)])
        self.assertEqual(self.ticket.assignee, LEE)
        self.assertIn("escalated", self.ticket.flags)

    def test_agent_reply_restarts_the_30_minutes(self):
        self.desk.clock.advance(minutes=20)
        add_reply(self.desk, self.ticket, BO, "Looking")
        self.desk.clock.advance(minutes=20)
        self.assertEqual(engine.run(self.desk), [])

    def test_requester_reply_does_not_restart_it(self):
        self.desk.clock.advance(minutes=20)
        add_reply(self.desk, self.ticket, ADA, "Anyone?")
        self.desk.clock.advance(minutes=10)
        self.assertEqual(engine.run(self.desk), [("stale-urgent", self.ticket.id)])

    def test_ticket_that_is_not_urgent_stays(self):
        other = ticket(self.desk, priority="high")
        self.desk.clock.advance(hours=3)
        engine.run(self.desk)
        self.assertIsNone(other.assignee)

    def test_ticket_goes_up_once(self):
        self.desk.clock.advance(minutes=45)
        engine.run(self.desk)
        self.assertEqual(engine.run(self.desk), [])

    def test_closed_ticket_is_not_escalated(self):
        status.close(self.desk, self.ticket)
        self.desk.clock.advance(hours=1)
        self.assertEqual(engine.run(self.desk), [])
        self.assertNotIn("escalated", self.ticket.flags)


class AutoClose(unittest.TestCase):
    def test_ticket_waiting_two_weeks_is_closed(self):
        desk = new_desk()
        made = ticket(desk)
        add_reply(desk, made, BO, "Is it still on fire?")
        desk.clock.advance(days=13)
        self.assertEqual(engine.run(desk), [])
        desk.clock.advance(days=1)
        self.assertEqual(engine.run(desk), [("auto-close", made.id)])
        self.assertEqual(made.status, "closed")
