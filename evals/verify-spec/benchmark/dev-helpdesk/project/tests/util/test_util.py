import datetime
import unittest

from helpdesk.util import dates, paging, text


class Util(unittest.TestCase):
    def test_shorten_cuts_long_text(self):
        self.assertEqual(text.shorten("a  b\nc"), "a b c")
        self.assertEqual(len(text.shorten("x" * 100)), 60)

    def test_slug(self):
        self.assertEqual(text.slug("Printer: on fire!"), "printer-on-fire")

    def test_age_in_words(self):
        self.assertEqual(dates.age_in_words(datetime.timedelta(minutes=59)), "59 min")
        self.assertEqual(dates.age_in_words(datetime.timedelta(hours=47)), "47 h")
        self.assertEqual(dates.age_in_words(datetime.timedelta(days=3)), "3 days")

    def test_paging(self):
        items = list(range(60))
        self.assertEqual(paging.page(items, 3, 25), list(range(50, 60)))
        self.assertEqual(paging.pages(items, 25), 3)
