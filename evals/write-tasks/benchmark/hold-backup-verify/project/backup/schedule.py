"""The nightly run, started by cron."""

import datetime

from backup.archive import write_archive
from backup.panel import set_light


def run(source, folder, today=None):
    """Write tonight's archive of source into folder. Returns its path."""
    today = today or datetime.date.today()
    target = write_archive(source, f"{folder}/backup-{today.isoformat()}.tar.gz")
    set_light("green")
    return target
