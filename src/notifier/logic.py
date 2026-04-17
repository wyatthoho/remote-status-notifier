import logging
import os
import psutil

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


def get_env_variable(key: str) -> str:
    var = os.getenv(key)
    if not var:
        msg = f'{key} environment variable is not set.'
        raise ValueError(msg)
    return var


def get_remote_user() -> str | None:
    users = [session.host for session in psutil.users() if session.host]
    if len(users) == 0:
        return None
    return users[0]


class SlackAgent:
    def __init__(self, token: str = None, channel_idx: str = None):
        self._token = token
        self._channel_idx = channel_idx
        self._client = WebClient(token=self._token)
        self.send_message('Slack agent created.')

    def send_message(self, message: str):
        try:
            self._client.chat_postMessage(
                channel=self._channel_idx,
                text=message
            )
            logger.info(f'Message sent: {message}')
        except SlackApiError as e:
            logger.info(f'Error sending message: {e.response['error']}')


class Detector:
    def __init__(self, commputer_name):
        self.commputer_name = commputer_name
        self.user_ori = None

    def run(self) -> str | None:
        user_ori = self.user_ori
        user_now = get_remote_user()
        
        # Update for next run
        self.user_ori = user_now

        if user_now == user_ori:
            return None

        # The user changed.
        if user_now:
            # Now, Someone in.
            return f'{user_now} has logged in!'
        else:
            # Now, Someone out
            return (
                f'{user_ori} has left. '
                f'The workstation {self.commputer_name} is currently idle.'
            )
