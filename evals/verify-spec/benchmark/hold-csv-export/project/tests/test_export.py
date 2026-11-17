import unittest

from reports.export import export


class Header(unittest.TestCase):
    def test_first_row_is_the_column_names(self):
        text = export(["id", "name"], [{"id": 1, "name": "Ada"}])
        self.assertEqual(text.splitlines()[0], "id,name")
