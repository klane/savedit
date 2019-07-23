import os

import dropbox

from savedit.config import DROPBOX_TOKEN
from savedit.integrations import Service


class Dropbox(Service):
    def __init__(self):
        self.dropbox = dropbox.Dropbox(DROPBOX_TOKEN)

    @staticmethod
    def check_post(post):
        return len(os.path.splitext(post.url)[1]) > 0

    @staticmethod
    def is_registered():
        return True

    def is_saved(self, post):
        pass

    def _save_post(self, post):
        pass
