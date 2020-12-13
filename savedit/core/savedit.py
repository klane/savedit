import os
from configparser import NoSectionError

from praw import Reddit

from .__version__ import __version__
from .database import DB, Post
from .plugin import PluginManager, load_plugins


def main():
    user_agent = f'savedit v{__version__} by /u/{os.environ["REDDIT_USERNAME"]}'

    try:
        reddit = Reddit(site_name='savedit', user_agent=user_agent)
    except NoSectionError:
        reddit = Reddit(
            client_id=os.environ['REDDIT_CLIENT_ID'],
            client_secret=os.environ['REDDIT_CLIENT_SECRET'],
            refresh_token=os.environ['REDDIT_REFRESH_TOKEN'],
            user_agent=user_agent,
        )

    plugins = reddit.config.CONFIG['savedit']['plugins'].split(',')
    load_plugins(plugins)

    user = reddit.user.me()
    saved_ids = [post.id for post in Post.select(Post.id)]
    new_posts = [post for post in user.saved() if post.id not in saved_ids]

    for post in new_posts:
        Post.create(post)
        PluginManager.hook.save_post(post=post)

    DB.close()
