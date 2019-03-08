from dropbox import Dropbox
from pocket import Pocket
from praw import Reddit
from pushbullet import PushBullet
from .config import *

reddit = Reddit(user_agent='savedit v0.1.0 by /u/{}'.format(REDDIT_USERNAME))

pb = PushBullet(PUSHBULLET_TOKEN)

db = Dropbox(DROPBOX_TOKEN)

pocket = Pocket(POCKET_KEY, POCKET_TOKEN)
