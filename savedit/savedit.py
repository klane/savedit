import os
import pkgutil
from configparser import NoSectionError

from praw import Reddit

from .__version__ import __version__
from .database import DB, Post
from .integrations import Notification, Service


def get_modules(packages):
    return [name for (_, name, _) in pkgutil.iter_modules(packages)]


def main():
    user_agent = 'savedit v{} by /u/{}'.format(__version__, os.environ['REDDIT_USERNAME'])
    notifications = Notification.get_registered()
    services = Service.get_registered()
    tables = [s.table for s in services] + [Post]
    DB.create_tables(tables)

    try:
        reddit = Reddit(site_name='savedit', user_agent=user_agent)
    except NoSectionError:
        reddit = Reddit(
            client_id=os.environ['REDDIT_CLIENT_ID'],
            client_secret=os.environ['REDDIT_CLIENT_SECRET'],
            refresh_token=os.environ['REDDIT_REFRESH_TOKEN'],
            user_agent=user_agent
        )

    user = reddit.user.me()
    saved_ids = [post.id for post in Post.select(Post.id)]
    new_posts = [post for post in user.saved() if post.id not in saved_ids]

    for post in new_posts:
        Post.create(post)
        selected_services = [s for s in services if s.check_post(post)]
        [s.save_post(post) for s in selected_services]
        [n.notify(post, selected_services) for n in notifications]

    DB.close()
