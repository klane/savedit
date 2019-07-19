import pkgutil

from praw import Reddit

from .__version__ import __version__
from .config import *
from .database import DB, Post
from .integrations import Service


def get_modules(packages):
    return [name for (_, name, _) in pkgutil.iter_modules(packages)]


def main():
    services = Service.get_registered()
    tables = [s.table() for s in services] + [Post]

    DB.drop_tables(tables)
    DB.create_tables(tables)

    reddit = Reddit('savedit', user_agent='savedit v{} by /u/{}'.format(__version__, REDDIT_USERNAME))
    user = reddit.user.me()
    [Post.create(post) for post in user.saved()]
    [s.table().create(post=post) for s in services for post in user.saved() if s.check_post(post)]
    DB.close()
