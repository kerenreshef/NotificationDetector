import logging
from datetime import datetime

from flask import Flask, request

from backend.utils import save_error_to_file
from events import PushEvent, TeamEvent, RepoEvent

logger = logging.getLogger(__name__)
app = Flask(__name__)

EVENT_HANDLERS = {
    'push': PushEvent(),
    'team': TeamEvent(),
    'repository': RepoEvent()
}


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
        error_msg = str(e)
        error_time = datetime.utcnow().isoformat()
        logger.error(f"An error occurred: {error_type} , while trying to process the event: {payload}.")
        save_error_to_file(payload, error_type, error_msg, error_time)

    return 'Webhook Received', 200


if __name__ == '__main__':
    app.run(debug=True)
