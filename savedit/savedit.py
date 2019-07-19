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
    tables = [s.table for s in services] + [Post]
    DB.create_tables(tables)

    reddit = Reddit('savedit', user_agent='savedit v{} by /u/{}'.format(__version__, REDDIT_USERNAME))
    user = reddit.user.me()
    saved_ids = [post.id for post in Post.select(Post.id)]
    new_posts = [post for post in user.saved() if post.id not in saved_ids]

    for post in new_posts:
        Post.create(post)
        selected_services = [s for s in services if s.check_post(post)]
        [s.table.create(post=post) for s in selected_services]

    DB.close()
