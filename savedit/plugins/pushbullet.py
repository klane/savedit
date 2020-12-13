import os

import pushbullet

from savedit.core import Notification
from savedit.core.plugin import hookimpl


class Pushbullet(Notification):
    def __init__(self):
        self.pushbullet = pushbullet.Pushbullet(os.environ['PUSHBULLET_TOKEN'])

    @hookimpl
    def notify(self, post, service):
        self.pushbullet.push_link(f'Reddit post saved to {service}', post.url)
