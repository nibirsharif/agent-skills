import unittest

from helpdesk.tickets import escalation, merge
from helpdesk.tickets.replies import add_reply
from tests.helpers import ADA, BO, LEE, new_desk, ticket


class Replies(unittest.TestCase):
    def setUp(self):
        self.desk = new_desk()
        self.ticket = ticket(self.desk)

    def test_reply_is_kept_with_its_time(self):
        self.desk.clock.advance(minutes=5)
        reply = add_reply(self.desk, self.ticket, ADA, "Still burning")
        self.assertEqual(self.ticket.replies, [reply])
        self.assertEqual(reply.at, self.desk.clock.now())

    def test_first_agent_to_reply_holds_the_ticket(self):
        add_reply(self.desk, self.ticket, BO, "On my way")
        add_reply(self.desk, self.ticket, LEE, "Me too")
        self.assertEqual(self.ticket.assignee, BO)

    def test_agent_reply_waits_on_the_requester(self):
        add_reply(self.desk, self.ticket, BO, "Is it still on fire?")
        self.assertIn("waiting", self.ticket.flags)
        add_reply(self.desk, self.ticket, ADA, "Yes")
        self.assertNotIn("waiting", self.ticket.flags)

    def test_last_agent_reply_ignores_the_requester(self):
        add_reply(self.desk, self.ticket, BO, "On my way")
        at = self.desk.clock.now()
        self.desk.clock.advance(minutes=10)
        add_reply(self.desk, self.ticket, ADA, "Hurry")
        self.assertEqual(self.ticket.last_agent_reply(), at)


class MergeAndLevels(unittest.TestCase):
    def test_merge_moves_replies_and_closes_the_duplicate(self):
        desk = new_desk()
        keep, duplicate = ticket(desk), ticket(desk)
        add_reply(desk, duplicate, ADA, "Same fire")
        merge.merge(desk, keep, duplicate)
        self.assertEqual(len(keep.replies), 1)
        self.assertEqual(duplicate.status, "closed")

    def test_levels(self):
        desk = new_desk()
        made = ticket(desk)
        self.assertEqual(escalation.level_of(made), "agent")
        made.assignee = LEE
        self.assertEqual(escalation.level_of(made), "lead")
        self.assertEqual(escalation.next_level("lead"), "manager")
        self.assertIsNone(escalation.next_level("manager"))
