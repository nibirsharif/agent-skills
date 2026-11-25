"""Notes kept in a JSON file. A note is a dict: id, text."""

import json
from pathlib import Path


class Store:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        return json.loads(self.path.read_text()) if self.path.exists() else []

    def save(self, notes):
        self.path.write_text(json.dumps(notes, indent=2))

    def add(self, text):
        notes = self.load()
        note = {"id": len(notes) + 1, "text": text}
        notes.append(note)
        self.save(notes)
        return note
