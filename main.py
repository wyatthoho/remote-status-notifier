import os
import time
import psutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


SLEEP_TIME = 20


def get_computer_name() -> str:
    '''Retrieve the computer name from environment variables.'''
    computer_name = os.getenv('COMPUTERNAME')
    if not computer_name:
        raise ValueError('COMPUTERNAME environment variable is not set.')
    return computer_name


def get_slack_token() -> str:
    '''Retrieve the Slack API token from environment variables.'''
    token = os.getenv('SLACK_TOKEN')
    if not token:
        raise ValueError('SLACK_TOKEN environment variable is not set.')
    return token


def get_slack_channel_idx() -> str:
    '''Retrieve the Slack channel index from environment variables.'''
    channel_idx = os.getenv('SLACK_CHANNEL_IDX')
    if not channel_idx:
        raise ValueError('SLACK_CHANNEL_IDX environment variable is not set.')
    return channel_idx


def get_remote_users() -> list[str]:
    '''Retrieve the currently logged-in remote desktop users.'''
    users = [session.host for session in psutil.users() if session.host]
    return users


def send_slack_message(client: WebClient, channel_idx: str, message: str):
    '''Send a message to the specified Slack channel.'''
    try:
        result = client.chat_postMessage(channel=channel_idx, text=message)
        print(f'Message sent: {message}')
    except SlackApiError as e:
        print(f'Error sending message: {e.response['error']}')


def main():
    commputer_name = get_computer_name()
    client = WebClient(token=get_slack_token())
    channel_idx = get_slack_channel_idx()
    first_run = True
    users_ori = []
    while True:
        users_now = get_remote_users()
        if not users_now:
            if users_ori:
                message = f'{", ".join(users_ori)} has left. The workstation {commputer_name} is currently idle.'
                send_slack_message(client, channel_idx, message)
            if first_run:
                message = f'The workstation {commputer_name} is currently idle.'
                send_slack_message(client, channel_idx, message)
        else:
            if users_now != users_ori:
                new_users = set(users_now) - set(users_ori)
                for user in new_users:
                    message = f'{user} has logged in!'
                    send_slack_message(client, channel_idx, message)
        users_ori = users_now
        first_run = False
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
