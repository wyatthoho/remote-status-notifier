import logging
import sys
import time
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
# from PIL import Image
# from pystray import Icon, Menu, MenuItem
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from notifier import logic

# ICON_IMG = Path(__file__).parent / 'icon' / 'favicon.ico'
# ICON_NAME = 'Remote Status Notifier'
LOG_PATH = Path.home() / 'remote-status-notifier.log'
SLEEP_TIME = 5


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_PATH,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s,%(msecs)03d [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


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
        self.user_now = logic.get_remote_user()

    def run(self) -> str | None:
        if self.user_now == self.user_ori:
            message = None

        # The user changed.
        if self.user_now:
            # Now, Someone in.
            message = f'{self.user_now} has logged in!'
        else:
            # Now, Someone out
            message = (
                f'{self.user_ori} has left. '
                f'The workstation {self.commputer_name} is currently idle.'
            )

        self.user_ori = self.user_now
        return message


def main():
    try:
        load_dotenv(find_dotenv())
        commputer_name = logic.get_env_variable('COMPUTERNAME')
        token = logic.get_env_variable('SLACK_TOKEN')
        channel_idx = logic.get_env_variable('SLACK_CHANNEL_IDX')
    except ValueError as e:
        print(f'Error reading variable: {e}')
        sys.exit(1)

    slack_agent = SlackAgent(token, channel_idx)
    detector = Detector(commputer_name)
    
    while True:
        message = detector.run()
        if message:
            slack_agent.send_message(message)
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
