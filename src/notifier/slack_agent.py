import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logger = logging.getLogger(__name__)


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
