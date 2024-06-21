# Notification Detector

### Project Build & Run Instructions:
1. Clone the project from the GitHub repository:
    https://github.com/kerenreshef/NotificationDetector
2. Install project requirements: 
   ```console
    pip install requirements.txt
    ```
3. Run the backend server:
   ```console
    python webhook_handler.py
    ```
4. Run ngrok tool for tunneling webhooks events from GitHub:
    ```console
    ngrok http 5000
    ```
5. Copy the forwarding generated url and set it as Payload URL when defining organization webhook.


### Project Unittests Running Instructions:
1. Open a terminal eindow and run the following command (from the project root): 
    ```console
    python -m unittest tests/unit_tests.py
    ```