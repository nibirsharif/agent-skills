import datetime
import io
import unittest

from todo import tasks as store
from todo.cli import main

TODAY = datetime.date(2026, 10, 20)


class Add(unittest.TestCase):
    def test_add_stores_the_due_date(self):
        tasks = []
        self.assertEqual(main(["add", "pay rent", "--due", "2026-11-01"], tasks, io.StringIO()), 0)
        self.assertEqual(tasks[0]["due"], datetime.date(2026, 11, 1))

    def test_invalid_date_prints_a_message(self):
        out = io.StringIO()
        main(["add", "pay rent", "--due", "next week"], [], out)
        self.assertEqual(out.getvalue(), "Invalid date: next week\n")


class Overdue(unittest.TestCase):
    def setUp(self):
        self.tasks = []
        store.add(self.tasks, "late", datetime.date(2026, 10, 19))
        store.add(self.tasks, "today", TODAY)
        store.add(self.tasks, "later", datetime.date(2026, 10, 21))

    def test_task_due_before_today_is_overdue(self):
        self.assertIn("late", [t["title"] for t in store.overdue(self.tasks, TODAY)])

    def test_task_due_today_is_not_overdue(self):
        self.assertNotIn("today", [t["title"] for t in store.overdue(self.tasks, TODAY)])

    def test_done_task_is_not_overdue(self):
        self.tasks[0]["done"] = True
        self.assertNotIn("late", [t["title"] for t in store.overdue(self.tasks, TODAY)])


class Listing(unittest.TestCase):
    def test_listing_keeps_every_task(self):
        tasks = []
        store.add(tasks, "no date")
        store.add(tasks, "second", datetime.date(2026, 11, 2))
        store.add(tasks, "first", datetime.date(2026, 11, 1))
        self.assertEqual(len(store.listing(tasks)), 3)
