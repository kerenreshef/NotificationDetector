import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def is_between_time_range(datetime_obj: datetime, start_time: str, end_time: str) -> bool:
    """
    This function checks if a datetime falls within a specific time range.

    :param datetime_obj: The datetime object.
    :param start_time: The start time of the range in 24-hour format.
    :param end_time: The end time of the range in 24-hour format.
    :return: True if the datetime is between start_time and end_time, False otherwise.
    """

    try:
        start_time_obj = datetime_obj.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime_obj.strptime(end_time, "%H:%M").time()
        datetime_time_obj = datetime_obj.time()
    except ValueError:
        logger.error(f"Invalid time format for start_time or end_time.")
        raise
    except AttributeError:
        logger.error(f"Invalid time format for datetime_obj.")
        raise

    return start_time_obj <= datetime_time_obj <= end_time_obj


def save_error_to_file(payload: dict, error_type: str, error_message: str, error_time: str) -> None:
    """
    Saves error information to a file named 'errors.log' in JSON format.
    :param error_time: The time which the error occurred.
    :param payload: The payload that caused the error.
    :param error_type: The type of error encountered.
    :param error_message: The error message associated with the exception.
    :return:
    """

    error_data = {
        "timestamp": error_time,
        "payload": payload,
        "error_type": error_type,
        "error_message": error_message,
    }

    with open("errors.log", "a") as error_file:
        json.dump(error_data, error_file)
