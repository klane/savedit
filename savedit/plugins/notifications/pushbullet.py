import os

import pushbullet

from savedit.core import Notification, plugin


class Pushbullet(Notification):
    name = 'Pushbullet'

    def __init__(self):
        self.pushbullet = pushbullet.Pushbullet(os.environ['PUSHBULLET_TOKEN'])

    @plugin.hookimpl
    def notify(self, post, services):
        for s in services:
            self.pushbullet.push_link(f'Reddit post saved to {s}', post.url)
