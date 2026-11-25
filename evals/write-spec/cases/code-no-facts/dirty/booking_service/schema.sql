CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    employee TEXT NOT NULL,
    room TEXT NOT NULL,
    day TEXT NOT NULL,         -- YYYY-MM-DD
    start_time TEXT NOT NULL,  -- HH:MM
    end_time TEXT NOT NULL     -- HH:MM
);
