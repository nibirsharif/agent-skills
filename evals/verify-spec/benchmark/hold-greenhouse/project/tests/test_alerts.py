import time
import unittest

from greenhouse.alerts import Monitor


class High(unittest.TestCase):
    def test_reading_above_35_raises_high(self):
        monitor = Monitor()
        self.assertEqual(monitor.reading(35.0, at=0), [])
        self.assertEqual(monitor.reading(35.1, at=1), ["high"])

    def test_no_second_high_alert(self):
        monitor = Monitor()
        monitor.reading(36.0, at=0)
        self.assertEqual(monitor.reading(37.0, at=1), [])

    def test_cool_reading_clears_the_alert(self):
        monitor = Monitor()
        monitor.reading(36.0, at=0)
        monitor.reading(30.0, at=1)
        self.assertNotIn("high", monitor.active)


class Log(unittest.TestCase):
    def test_alert_is_logged(self):
        monitor = Monitor()
        raised = monitor.reading(36.0, at=10)
        self.assertEqual(raised, ["high"])


class Speed(unittest.TestCase):
    def test_reading_is_fast(self):
        monitor = Monitor()
        for n in range(1000):
            started = time.perf_counter()
            monitor.reading(20.0 + n % 20, at=n)
            self.assertLess(time.perf_counter() - started, 0.010)
