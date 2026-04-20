import logging
import sys
import threading
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from PIL import Image
from pystray import Icon, Menu, MenuItem

from notifier.utils import get_env_variable
from notifier.slack_agent import SlackAgent
from notifier.user_detector import UserDetector


ICON_IMG = Path(__file__).parent / 'icon' / 'favicon.ico'
ICON_NAME = 'Remote Status Notifier'
LOG_PATH = Path.home() / 'remote-status-notifier.log'
SLEEP_TIME = 10


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_PATH,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s,%(msecs)03d [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


class App:
    def __init__(self):
        self.computer_name, self.token, self.channel_idx = self._load_env_config()
        self.menu = self._build_menu()
        self.icon = self._build_icon()

        self._main_event = threading.Event()
        self._start_main_thread()
        self.icon.run()

    def _load_env_config(self) -> tuple[str, str, str]:
        try:
            load_dotenv(find_dotenv())
            computer_name = get_env_variable('COMPUTERNAME')
            token = get_env_variable('SLACK_TOKEN')
            channel_idx = get_env_variable('SLACK_CHANNEL_IDX')
        except ValueError as e:
            logger.error(f'Error reading variable: {e}')
            sys.exit(1)
        return computer_name, token, channel_idx

    def _build_menu(self) -> Menu:
        return Menu(
            MenuItem(
                text='Close',
                action=self.on_close,
            )
        )

    def _build_icon(self):
        return Icon(
            name=ICON_NAME,
            title=ICON_NAME,
            icon=Image.open(Path(ICON_IMG)),
            menu=self.menu
        )

    def _start_main_thread(self) -> None:
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        agent = SlackAgent(self.token, self.channel_idx)
        detector = UserDetector(self.computer_name)
        logger.info('Main call started')

        while not self._main_event.is_set():
            message = detector.check_user_state()
            if message:
                agent.send_message(message)
            self._main_event.wait(SLEEP_TIME)

        logger.info('Main call stopped.')

    def on_close(self, icon, item):
        self._main_event.set()
        icon.stop()
        logger.info('App closed.')


if __name__ == '__main__':
    App()
