from configparser import NoSectionError
from itertools import chain

import yaml
from praw import Reddit

from .__version__ import __version__
from .plugin import PluginManager, load_plugins


def main():
    with open('savedit.yml') as f:
        config = yaml.safe_load(f)

    load_plugins(config)
    user_agent = f'savedit v{__version__} by /u/{config["reddit"]["username"]}'

    try:
        reddit = Reddit(site_name='savedit', user_agent=user_agent)
    except NoSectionError:
        reddit = Reddit(
            client_id=config['reddit']['client_id'],
            client_secret=config['reddit']['client_secret'],
            refresh_token=config['reddit']['refresh_token'],
            user_agent=user_agent,
        )

    user = reddit.user.me()
    saved_ids = [post['id'] for post in chain(*PluginManager.hook.select_posts())]
    new_posts = [post for post in user.saved() if post.id not in saved_ids]

    for post in new_posts:
        services = PluginManager.hook.run_service(post=post)
        PluginManager.hook.insert_post(post=post, plugins=services)
        PluginManager.hook.notify(post=post, services=services)

    PluginManager.hook.close()
