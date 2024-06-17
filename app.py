from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_webhook():
    # Access the webhook payload data (JSON format)
    data = request.get_json()
    print(data)
    # Process the payload based on its type (e.g., push, pull_request)
    # if data['action'] == 'push':
    #     # Handle push events (e.g., update code in your application)
    #     print(f"Received push event: {data}")
    # elif data['action'] == 'pull_request':
    #     # Handle pull request events (e.g., review code changes)
    #     print(f"Received pull request event: {data}")
    # else:
    #     # Handle other event types if needed
    #     print(f"Received unknown event: {data}")

    return 'Webhook Received', 200  # Return a success response


if __name__ == '__main__':
    app.run(debug=True)
