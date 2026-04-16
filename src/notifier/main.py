import sys
import time

from dotenv import load_dotenv, find_dotenv

from notifier import logic

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


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

    user_ori = ''
    while True:
        message = ''
        user_now = logic.get_remote_users()[0]

        if user_now:
            # Workstation is occupied now.
            if user_now == user_ori:
                # Occupied by the same user. -> State not change.
                ...
            else:
                # Occupied by a different user. -> State changed.
                message = f'{user_now} has logged in!'
        else:
            # Workstation is free now.
            if user_ori == '':
                # Originally free. -> State not change.
                ...
            else:
                # Originally occupied. -> State changed.
                message = (
                    f'{", ".join(user_ori)} has left. '
                    f'The workstation {commputer_name} is currently idle.'
                )

        user_ori = user_now

        if message:
            slack_agent.send_message(message)

        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
