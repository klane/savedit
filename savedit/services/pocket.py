import os

from pocket import Pocket

from savedit.config import POCKET_KEY, POCKET_TOKEN
from savedit.integrations import Service


class PocketService(Service):
    def __init__(self):
        self.pocket = Pocket(POCKET_KEY, POCKET_TOKEN)

    @staticmethod
    def check_post(post):
        return len(os.path.splitext(post.url)[1]) == 0

    @staticmethod
    def is_registered():
        return True

    def is_saved(self, post):
        pass

    def save_post(self, post):
        pass

    @classmethod
    def table_name(cls):
        return 'pocket'
