import pushbullet

from savedit.core import Notification, plugin


class Pushbullet(Notification):
    name = 'Pushbullet'

    def __init__(self, config):
        self.config = config
        self.pushbullet = pushbullet.Pushbullet(config['token'])

    @plugin.hookimpl
    def notify(self, post, services):
        for s in services:
            self.pushbullet.push_link(f'Reddit post saved to {s}', post.url)
