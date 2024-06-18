import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def is_between_time_range(datetime_obj, start_time, end_time):
    """
    This function checks if a datetime falls within a specific time range.

    :param datetime_obj: The datetime object.
    :param start_time: The start time of the range in 24-hour format.
    :param end_time: The end time of the range in 24-hour format.
    :return: True if the timestamp is between start_time and end_time, False otherwise.
    """

    # try:
    #     # Parse timestamp string to datetime object. Assuming specific format
    #     timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
    # except ValueError:
    #     logger.error(f"Invalid timestamp format. Returning False.")
    #     return False

    # Parse start and end times as datetime objects
    try:
        start_time_obj = datetime_obj.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime_obj.strptime(end_time, "%H:%M").time()
    except ValueError:
        print(f"Invalid time format for start_time or end_time.")
        return False

    # Extract time portion from the timestamp
    timestamp_time_obj = datetime_obj.time()

    return start_time_obj <= timestamp_time_obj <= end_time_obj
