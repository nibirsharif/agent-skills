"""Book and cancel a room."""

import sqlite3


def book(db, employee, room, day, start_time, end_time):
    """Store a booking. Returns (HTTP status, booking ID)."""
    try:
        cursor = db.execute(
            "INSERT INTO bookings (employee, room, day, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
            (employee, room, day, start_time, end_time),
        )
    except sqlite3.IntegrityError:
        # schema.sql: UNIQUE (room, day)
        return 409, None
    db.commit()
    return 201, cursor.lastrowid


def cancel(db, booking_id):
    """Mark a booking as cancelled. purge.py deletes it later."""
    db.execute("UPDATE bookings SET cancelled_at = datetime('now') WHERE id = ?", (booking_id,))
    db.commit()
    return 204
