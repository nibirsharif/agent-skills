"""A room's bookings as an iCalendar file."""


def calendar(bookings):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0"]
    for booking in bookings:
        lines += [
            "BEGIN:VEVENT",
            f"UID:booking-{booking.id}",
            f"DTSTART:{booking.start:%Y%m%dT%H%M%S}",
            f"DTEND:{booking.end:%Y%m%dT%H%M%S}",
            f"SUMMARY:{booking.room}",
            "END:VEVENT",
        ]
    return "\r\n".join(lines + ["END:VCALENDAR"]) + "\r\n"
