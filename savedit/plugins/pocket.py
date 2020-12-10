import os

import pocket

from savedit.core import Service


class Pocket(Service):
    def __init__(self):
        self.pocket = pocket.Pocket(
            os.environ['POCKET_KEY'], os.environ['POCKET_TOKEN']
        )

    @staticmethod
    def check_post(post):
        return len(os.path.splitext(post.url)[1]) == 0

    @staticmethod
    def is_registered():
        return True

    def is_saved(self, post):
        pass

    def _save_post(self, post):
        pass
