FR-001: When an employee books a room for a time slot, the booking service shall store the booking and return the booking ID.

FR-002: If an employee books a room for a time slot that overlaps a stored booking of that room, then the booking service shall reject the booking and return HTTP status 409.

FR-003: When an employee cancels a booking, the booking service shall mark the booking as cancelled.

Q-001: `booking_service/schema.sql` allows one booking of a room for each day: does the booking service reject a booking of a room that already has a stored booking on that day for a time slot that does not overlap?

Q-002: `booking_service/purge.py` deletes a cancelled booking 7 days after the booking was cancelled, and the input says 30 days as today: how many days after a booking was cancelled does the booking service delete the booking?
