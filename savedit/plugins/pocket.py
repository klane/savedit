import os

import pocket

from savedit.core import Service


class Pocket(Service):
    def __init__(self):
        self.pocket = pocket.Pocket(
            os.environ['POCKET_KEY'], os.environ['POCKET_TOKEN']
        )

    def check_post(self, post):
        return len(os.path.splitext(post.url)[1]) == 0

    def is_saved(self, post):
        pass

    def _save_post(self, post):
        pass
