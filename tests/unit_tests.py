import unittest
from datetime import datetime, timedelta

from backend.utils import is_between_time_range


class TestTimeRangeCheck(unittest.TestCase):

    def setUp(self):
        """Sets up common datetime objects for tests."""
        self.base_time = datetime(year=2024, month=6, day=19)  # 00:00
        self.within_range = self.base_time + timedelta(hours=15)  # 15:00
        self.before_range = self.base_time + timedelta(hours=13)  # 13:00
        self.after_range = self.base_time + timedelta(hours=17)  # 17:00
        self.invalid_time_format = "invalid datetime format"
        self.invalid_start_time = "invalid time"
        self.start_time = "14:00"
        self.end_time = "16:00"

    def test_time_within_range(self):
        """Tests if a datetime object within the range returns True."""
        self.assertTrue(is_between_time_range(self.within_range, self.start_time, self.end_time))

    def test_time_before_range(self):
        """Tests if a datetime object before the range returns False."""
        self.assertFalse(is_between_time_range(self.before_range, self.start_time, self.end_time))

    def test_time_after_range(self):
        """Tests if a datetime object after the range returns False."""
        self.assertFalse(is_between_time_range(self.after_range, self.start_time, self.end_time))

    def test_invalid_time_format(self):
        """Tests if an invalid start time format raises an error (using logging)."""

        with self.assertRaises(ValueError):
            is_between_time_range(self.base_time, self.invalid_start_time, self.end_time)

    def test_invalid_datetime_format(self):
        """Tests if an invalid datetime object raises an error."""
        with self.assertRaises(AttributeError):
            is_between_time_range(self.invalid_time_format, self.start_time, self.end_time)


if __name__ == "__main__":
    unittest.main()
