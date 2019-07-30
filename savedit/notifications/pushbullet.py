import os

import pushbullet

from savedit.integrations import Notification


class Pushbullet(Notification):
    def __init__(self):
        self.pushbullet = pushbullet.Pushbullet(os.environ['PUSHBULLET_TOKEN'])

    @staticmethod
    def is_registered():
        return True

    def notify(self, post, services):
        if len(services) == 1:
            service_str = str(services[0])
        else:
            first = ', '.join([str(s) for s in services[:-1]])
            service_str = '{} & {}'.format(first, services[-1])

        self.pushbullet.push_link('Reddit post saved to ' + service_str, post.url)
