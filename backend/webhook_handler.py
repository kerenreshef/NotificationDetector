import json
import logging
from datetime import datetime

from flask import Flask, request

from events import PushEvent, TeamEvent, RepoEvent

logger = logging.getLogger(__name__)
app = Flask(__name__)

EVENT_HANDLERS = {
    'push': PushEvent(),
    'team': TeamEvent(),
    'repository': RepoEvent()
}


def save_error_to_file(payload: dict, error_type: str, error_message: str) -> None:
    """
    Saves error information to a file named 'errors.log' in JSON format.
    :param payload: The payload that caused the error.
    :param error_type: The type of error encountered.
    :param error_message: The error message associated with the exception.
    :return:
    """

    error_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload,
        "error_type": error_type,
        "error_message": error_message,
    }

    with open("errors.log", "a") as error_file:
        json.dump(error_data, error_file)


@app.route('/', methods=['POST'])
def handle_webhook():
    payload = request.get_json()

    event_type = request.headers.get("X-GitHub-Event")
    try:
        if event_type in EVENT_HANDLERS:
            EVENT_HANDLERS[event_type].handle(payload)
        else:
            logger.debug(f"Unknown event type: {event_type}")
    except Exception as e:
        error_type = type(e).__name__
        logger.error(f"An error occurred: {error_type} , while trying to process the event: {payload}.")
        save_error_to_file(payload, error_type, str(e))

    return 'Webhook Received', 200


if __name__ == '__main__':
    app.run(debug=True)
