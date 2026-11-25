"""Book a room."""


def book(db, employee, room, day, start_time, end_time):
    """Store a booking. Returns the HTTP status."""
    taken = db.execute(
        "SELECT 1 FROM bookings WHERE room = ? AND day = ? AND start_time < ? AND end_time > ?",
        (room, day, end_time, start_time),
    ).fetchone()
    if taken:
        return 400
    db.execute(
        "INSERT INTO bookings (employee, room, day, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
        (employee, room, day, start_time, end_time),
    )
    db.commit()
    return 200
