import json
import os
import unittest
from datetime import datetime, timedelta

from backend.utils import is_between_time_range, save_error_to_file


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


class TestSaveErrorToFile(unittest.TestCase):

    def test_save_error_data_and_check_file(self):
        """
        Tests if error data is written to the file in JSON format and the file is created.
        """
        payload = {"key": "value"}
        error_type = "TestError"
        error_message = "An error occurred."
        error_time = datetime.utcnow().isoformat()

        save_error_to_file(payload, error_type, error_message, error_time)

        expected_data = {
            "timestamp": error_time,
            "payload": payload,
            "error_type": error_type,
            "error_message": error_message,
        }

        # assert that the errors file exists
        self.assertTrue(os.path.exists("errors.log"))

        # open the file read its contents
        with open("errors.log", "r") as error_file:
            actual_data = json.load(error_file)

        self.assertEqual(actual_data, expected_data)

    def tearDown(self):
        """Deletes the created 'errors.log' file after the test."""
        if os.path.exists("errors.log"):
            os.remove("errors.log")


if __name__ == "__main__":
    unittest.main()
