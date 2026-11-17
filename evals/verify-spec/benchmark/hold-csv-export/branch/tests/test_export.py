import datetime
import unittest

from reports.export import export


class Header(unittest.TestCase):
    def test_first_row_is_the_column_names(self):
        text = export(["id", "name"], [{"id": 1, "name": "Ada"}])
        self.assertEqual(text.splitlines()[0], "id,name")


class Values(unittest.TestCase):
    def test_none_is_an_empty_field(self):
        text = export(["id", "name"], [{"id": 1, "name": None}])
        self.assertEqual(text.splitlines()[1], "1,")

    def test_date_is_written(self):
        text = export(["day"], [{"day": datetime.date(2026, 3, 9)}])
        self.assertIn("2026", text.splitlines()[1])


class Limits(unittest.TestCase):
    def test_large_report(self):
        rows = [{"id": n} for n in range(10_001)]
        text = export(["id"], rows)
        self.assertTrue(text)
