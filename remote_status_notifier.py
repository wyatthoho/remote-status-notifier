import time
import psutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


SLACK_TOKEN = 'xoxb-443261833458-8229610109394-zCOFDQr5byxDKncftGuQr9t8'
CHANNEL_NAME = 'slackbot-test'
SLEEP_TIME = 30
client = WebClient(token=SLACK_TOKEN)


def get_conversation_id() -> str:
    '''Fetch the conversation ID for the specified channel name.'''
    try:
        for result in client.conversations_list():
            for channel in result['channels']:
                if channel['name'] == CHANNEL_NAME:
                    print(f'Found conversation ID: {channel['id']}')
                    return channel['id']
    except SlackApiError as e:
        print(f'Error fetching conversation ID: {e.response['error']}')
    return None


def get_remote_users():
    '''Retrieve the currently logged-in remote desktop users.'''
    users = [session.host for session in psutil.users() if session.host]
    return users


def send_slack_message(conversation_id, message):
    '''Send a message to the specified Slack channel.'''
    try:
        result = client.chat_postMessage(channel=conversation_id, text=message)
        print(f'Message sent: {message}')
    except SlackApiError as e:
        print(f'Error sending message: {e.response['error']}')


def monitor_remote_users(conversation_id):
    '''Monitor remote desktop users and notify Slack of status changes.'''
    last_status = None
    while True:
        remote_users = get_remote_users()
        status = (
            f'The workstation is currently in use by: {', '.join(remote_users)}'
            if remote_users else
            'The workstation is currently idle.'
        )
        if status != last_status:
            send_slack_message(conversation_id, status)
            last_status = status
        time.sleep(SLEEP_TIME)


def main():
    conversation_id = get_conversation_id()
    if conversation_id:
        monitor_remote_users(conversation_id)
    else:
        print('Unable to find the specified Slack channel.')


if __name__ == '__main__':
    main()
