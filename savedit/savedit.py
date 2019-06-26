from praw import Reddit
from pushbullet import PushBullet

from __version__ import __version__
from config import *
from services import DatabaseService


class Savedit(Reddit):
    def __init__(self, site_name=None, requestor_class=None, requestor_kwargs=None, **config_settings):
        super(Savedit, self).__init__(
            site_name=site_name,
            requestor_class=requestor_class,
            requestor_kwargs=requestor_kwargs,
            **config_settings
        )

        self.db = DatabaseService('../savedit.db')
        self.db.reset()


savedit = Savedit('savedit', user_agent='savedit v{} by /u/{}'.format(__version__, REDDIT_USERNAME))
user = savedit.user.me()
[savedit.db.save_post(post) for post in user.saved()]
savedit.db.commit()
savedit.db.close()

pb = PushBullet(PUSHBULLET_TOKEN)
