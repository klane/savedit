import os

import pushbullet

from savedit.core import Notification


class Pushbullet(Notification):
    def __init__(self):
        self.pushbullet = pushbullet.Pushbullet(os.environ['PUSHBULLET_TOKEN'])

    def notify(self, post, services):
        if len(services) == 1:
            service_str = str(services[0])
        else:
            first = ', '.join([str(s) for s in services[:-1]])
            service_str = f'{first} & {services[-1]}'

        self.pushbullet.push_link('Reddit post saved to ' + service_str, post.url)
