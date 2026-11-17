"""Temperature alerts for the greenhouse monitor. Times are seconds."""

HIGH_ABOVE = 35.0
CLEAR_AT = 35.0
SENSOR_LOST_AFTER = 120


class Monitor:
    def __init__(self):
        self.active = set()
        self.last_reading_at = None

    def reading(self, celsius, at):
        """Take a temperature reading. Returns the alerts it raised."""
        self.last_reading_at = at
        self.active.discard("sensor-lost")
        if celsius > HIGH_ABOVE:
            if "high" not in self.active:
                self.active.add("high")
                return ["high"]
        elif celsius <= CLEAR_AT:
            self.active.discard("high")
        return []

    def tick(self, at):
        """Called once a second. Returns the alerts it raised."""
        if self.last_reading_at is None or "sensor-lost" in self.active:
            return []
        if at - self.last_reading_at >= SENSOR_LOST_AFTER:
            self.active.add("sensor-lost")
            return ["sensor-lost"]
        return []
