"""Write a folder as a tar archive."""

import tarfile
from pathlib import Path


def write_archive(source, target):
    """Write the folder source as the gzip tar archive target. Returns target as a Path."""
    target = Path(target)
    with tarfile.open(target, "w:gz") as archive:
        archive.add(source, arcname=Path(source).name)
    return target
