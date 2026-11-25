import io
import tempfile
import unittest
from pathlib import Path

from notes.cli import main


class List(unittest.TestCase):
    def test_list_prints_every_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.json"
            main(["add", "buy milk"], io.StringIO(), path)
            out = io.StringIO()
            main(["list"], out, path)
            self.assertEqual(out.getvalue(), "1  buy milk\n")
