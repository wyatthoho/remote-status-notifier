import logging
import psutil

logger = logging.getLogger(__name__)


class UserDetector:
    def __init__(self, commputer_name):
        self.commputer_name = commputer_name
        self.user_ori = None

    def get_remote_user(self) -> str | None:
        users = [session.host for session in psutil.users() if session.host]
        if len(users) == 0:
            return None
        return users[0]

    def check_user_state(self) -> str | None:
        user_ori = self.user_ori
        user_now = self.get_remote_user()

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
