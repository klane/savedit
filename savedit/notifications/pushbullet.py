from pushbullet import Pushbullet

from savedit.config import PUSHBULLET_TOKEN
from savedit.integrations import Notification


class PushbulletNotification(Notification):
    def __init__(self):
        self.pb = Pushbullet(PUSHBULLET_TOKEN)

    @staticmethod
    def is_registered():
        return True

    def notify(self, post):
        pass
