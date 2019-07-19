from pushbullet import PushBullet

from savedit.config import PUSHBULLET_TOKEN
from savedit.integrations import Notification


class PushbulletNotification(Notification):
    def __init__(self):
        self.pb = PushBullet(PUSHBULLET_TOKEN)

    @staticmethod
    def is_registered():
        return True

    def notify(self, post):
        pass
