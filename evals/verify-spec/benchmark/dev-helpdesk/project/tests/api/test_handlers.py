import unittest

from helpdesk.api import router
from tests.helpers import ADA, BO, LEE, SUPPORT, new_desk, ticket


class Requests(unittest.TestCase):
    def setUp(self):
        self.desk = new_desk()

    def test_post_ticket_opens_one(self):
        made = router.dispatch(self.desk, "POST", "/tickets", ADA, subject="No sound", team=SUPPORT)
        self.assertEqual(made.requester, ADA)

    def test_post_reply_adds_it(self):
        made = ticket(self.desk)
        router.dispatch(self.desk, "POST", "/tickets/reply", ADA, ticket_id=made.id, body="Hello?")
        self.assertEqual(made.replies[0].body, "Hello?")

    def test_post_close_closes(self):
        made = ticket(self.desk)
        router.dispatch(self.desk, "POST", "/tickets/close", BO, ticket_id=made.id)
        self.assertEqual(made.status, "closed")

    def test_agent_hands_a_ticket_to_the_lead(self):
        made = ticket(self.desk)
        router.dispatch(self.desk, "POST", "/tickets/handoff", BO, ticket_id=made.id)
        self.assertEqual(made.assignee, LEE)
        self.assertEqual(made.escalated_at, self.desk.clock.now())

    def test_unknown_request_has_no_route(self):
        with self.assertRaises(router.NoRoute):
            router.dispatch(self.desk, "GET", "/nothing", BO)
