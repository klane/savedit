from praw import Reddit

from __version__ import __version__
from config import *
from database import DB, TABLES, Post

DB.drop_tables(TABLES)
DB.create_tables(TABLES)

reddit = Reddit('savedit', user_agent='savedit v{} by /u/{}'.format(__version__, REDDIT_USERNAME))
user = reddit.user.me()
[Post.create(post) for post in user.saved()]
DB.close()
