import os
import time
import psutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


NAME_WORKSTATION = 'TEST'
CHANNEL_NAME = 'slackbot-test'
SLEEP_TIME = 20


def get_slack_token() -> str:
    '''Retrieve the Slack API token from environment variables.'''
    token = os.getenv('SLACK_TOKEN')
    if not token:
        raise ValueError('SLACK_TOKEN environment variable is not set.')
    return token


def get_remote_users() -> list[str]:
    '''Retrieve the currently logged-in remote desktop users.'''
    users = [session.host for session in psutil.users() if session.host]
    return users


def get_channel_idx(client: WebClient, channel_name: str) -> str:
    '''Fetch the conversation ID for the specified channel name.'''
    try:
        for result in client.conversations_list():
            for channel in result['channels']:
                if channel['name'] == channel_name:
                    print(f'Found conversation ID: {channel['id']}')
                    return channel['id']
    except SlackApiError as e:
        print(f'Error fetching conversation ID: {e.response['error']}')
    return None


def send_slack_message(client: WebClient, channel_idx: str, message: str):
    '''Send a message to the specified Slack channel.'''
    try:
        result = client.chat_postMessage(channel=channel_idx, text=message)
        print(f'Message sent: {message}')
    except SlackApiError as e:
        print(f'Error sending message: {e.response['error']}')


def main():
    client = WebClient(token=get_slack_token())
    channel_idx = get_channel_idx(client, CHANNEL_NAME)
    first_run = True
    users_ori = []
    while True:
        users_now = get_remote_users()
        if not users_now:
            if users_ori:
                message = f'{", ".join(users_ori)} has left. The workstation {NAME_WORKSTATION} is currently idle.'
                send_slack_message(client, channel_idx, message)
            if first_run:
                message = f'The workstation {NAME_WORKSTATION} is currently idle.'
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
