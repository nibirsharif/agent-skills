import tarfile
import tempfile
import unittest
from pathlib import Path

from backup.archive import write_archive


class WriteArchive(unittest.TestCase):
    def test_archive_holds_the_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "photos"
            source.mkdir()
            (source / "a.txt").write_text("a")
            target = write_archive(source, Path(tmp) / "out.tar.gz")
            with tarfile.open(target) as archive:
                self.assertIn("photos/a.txt", archive.getnames())
