import os

import dropbox

from savedit.core import Service


class Dropbox(Service):
    name = 'Dropbox'

    def __init__(self, config):
        self.config = config
        self.dropbox = dropbox.Dropbox(config['token'])

    def check_post(self, post):
        return len(os.path.splitext(post.url)[1]) > 0

    def save_post(self, post):
        pass
