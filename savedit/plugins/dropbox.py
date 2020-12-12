import os

import dropbox

from savedit.core import Service


class Dropbox(Service):
    def __init__(self):
        self.dropbox = dropbox.Dropbox(os.environ['DROPBOX_TOKEN'])

    @staticmethod
    def check_post(post):
        return len(os.path.splitext(post.url)[1]) > 0

    def is_saved(self, post):
        pass

    def _save_post(self, post):
        pass
