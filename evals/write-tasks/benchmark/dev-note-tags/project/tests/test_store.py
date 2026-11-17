import tempfile
import unittest
from pathlib import Path

from notes.store import Store


class Add(unittest.TestCase):
    def test_add_saves_the_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp) / "notes.json")
            store.add("buy milk")
            self.assertEqual(store.load(), [{"id": 1, "text": "buy milk"}])
