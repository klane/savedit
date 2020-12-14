import os

import dropbox

from savedit.core import Service


class Dropbox(Service):
    def __init__(self):
        self.dropbox = dropbox.Dropbox(os.environ['DROPBOX_TOKEN'])

    def check_post(self, post):
        return len(os.path.splitext(post.url)[1]) > 0

    def save_post(self, post):
        pass
