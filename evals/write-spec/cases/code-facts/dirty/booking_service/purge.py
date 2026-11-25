"""Delete cancelled bookings. Cron runs purge() once a day."""

PURGE_AFTER_DAYS = 7


def purge(db):
    """Delete every booking that was cancelled more than PURGE_AFTER_DAYS days ago."""
    db.execute(
        "DELETE FROM bookings WHERE cancelled_at < datetime('now', ?)",
        (f"-{PURGE_AFTER_DAYS} days",),
    )
    db.commit()
