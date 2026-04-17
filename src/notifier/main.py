import sys
import time

from dotenv import load_dotenv, find_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from notifier import logic


SLEEP_TIME = 5


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
            print(f'Message sent: {message}')
        except SlackApiError as e:
            print(f'Error sending message: {e.response['error']}')


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

    user_ori = None
    while True:
        user_now = logic.get_remote_user()

        if user_now == user_ori:
            continue

        # The user changed.
        if user_now:
            # Now, Someone in.
            message = f'{user_now} has logged in!'
        else:
            # Now, Someone out
            message = (
                f'{user_ori} has left. '
                f'The workstation {commputer_name} is currently idle.'
            )

        user_ori = user_now

        if message:
            slack_agent.send_message(message)

        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
