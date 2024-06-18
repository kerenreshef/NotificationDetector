import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def is_between_time_range(timestamp_str, start_time, end_time):
    """
    This function checks if a timestamp in string format falls within a specific time range.

    :param timestamp_str: The timestamp string in a format parsable by datetime.strptime.
    :param start_time: The start time of the range in 24-hour format.
    :param end_time: The end time of the range in 24-hour format.
    :return: True if the timestamp is between start_time and end_time, False otherwise.
    """

    try:
        # Parse timestamp string to datetime object. Assuming specific format
        timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        logger.error(f"Invalid timestamp format. Returning False.")
        return False

    # Parse start and end times as datetime objects
    try:
        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()
    except ValueError:
        print(f"Invalid time format for start_time or end_time.")
        return False

    # Extract time portion from the timestamp
    timestamp_time_obj = timestamp_obj.time()

    return start_time_obj <= timestamp_time_obj <= end_time_obj
