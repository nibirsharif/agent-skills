Requirements for the booking service:

- When an employee books a room for a time slot, the booking service stores the booking and returns the booking ID.
- If an employee books a room for a time slot that overlaps a stored booking of that room, the booking service rejects the booking and returns HTTP status 409.
