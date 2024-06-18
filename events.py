import logging
from abc import ABC, abstractmethod
from datetime import datetime

from utils import is_between_time_range

logger = logging.getLogger(__name__)


class GitHubEvent(ABC):
    """Abstract base class representing a GitHub event."""

    event_type: str
    received_at: datetime
    time_format: str

    def __init__(self, event_type):
        self.event_type = event_type
        self.received_at = datetime.utcnow()

    @abstractmethod
    def handle(self, data: dict):
        """Abstract method to handle the specific event type."""
        pass


class PushEvent(GitHubEvent):
    """Event handler for Push events."""

    def __init__(self):
        super().__init__('push')

    def handle(self, data: dict):
        repository = data.get("repository")
        pushed_timestamp = repository.get("pushed_at")
        repo_name = repository.get("name")
        # start_time = "14:00"
        # end_time = "16:00"
        start_time = "03:00"
        end_time = "05:00"
        if is_between_time_range(pushed_timestamp, start_time, end_time):
            logger.warning(f"Suspicious behavior detected: pushing code to repo {repo_name} between {start_time}-{end_time}")


class RepoEvent(GitHubEvent):
    """Event handler for repository events."""

    def __init__(self):
        super().__init__('repository')
        self.time_format = '%Y-%m-%dT%H:%M:%SZ'
        self.action_handlers = {
            'deleted': self._handle_delete,
        }

    def handle(self, data: dict):
        action = data.get("action")

        # Check if an action handler exists for this event
        if action in self.action_handlers:
            self.action_handlers[action](data)
        else:
            logger.error(f"Unknown Team event action: {action}")

    def _handle_delete(self, data):
        repo_obj = data.get("repository")
        repo_name = repo_obj.get("name")
        repo_create_str = repo_obj.get("created_at")
        try:
            repo_create_datetime = datetime.strptime(repo_create_str, self.time_format)
        except ValueError:
            logger.error(f"Failed to parse creation time: {repo_create_str}. does not match the format: {self.time_format}")
            raise

        # calculate time diff
        time_diff = self.received_at - repo_create_datetime
        minutes_diff = time_diff.total_seconds() / 60
        if minutes_diff < 10:
            logger.warning(
                f"Suspicious behavior detected: repository {repo_name} was created and deleted in less than 10 minutes")


class TeamEvent(GitHubEvent):
    """Event handler for team events."""

    def __init__(self):
        super().__init__('team')
        self.action_handlers = {
            'created': self._handle_create,
        }

    def handle(self, data: dict):
        action = data.get("action")

        # Check if an action handler exists for this event
        if action in self.action_handlers:
            self.action_handlers[action](data)
        else:
            logger.error(f"Unknown Team event action: {action}")

    def _handle_create(self, data: dict):
        team_name: str = data.get("team").get("name")
        if team_name.lower().startswith("hacker"):
            logger.warning(f"Suspicious behavior detected: team {team_name} was created with the prefix 'hacker'.")

