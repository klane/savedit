import os

import pocket

from savedit.core import Service


class Pocket(Service):
    name = 'Pocket'

    def __init__(self, config):
        self.config = config
        self.pocket = pocket.Pocket(config['key'], config['token'])

    def check_post(self, post):
        return len(os.path.splitext(post.url)[1]) == 0

    def save_post(self, post):
        pass
