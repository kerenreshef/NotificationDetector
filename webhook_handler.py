import logging

from flask import Flask, request

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

    if event_type in EVENT_HANDLERS:
        EVENT_HANDLERS[event_type].handle(payload)
    else:
        logger.error(f"Unknown event type: {event_type}")

    return 'Webhook Received', 200


if __name__ == '__main__':
    app.run(debug=True)
