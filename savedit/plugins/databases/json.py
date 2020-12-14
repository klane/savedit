from tinydb import TinyDB

from savedit.core import Database, plugin

DATABASE_FILE = 'savedit.json'
POST_FIELDS = (
    'id',
    'created_utc',
    'title',
    'is_self',
    'selftext',
    'permalink',
    'url',
    'subreddit',
)


class Json(Database):
    def __init__(self):
        self.db = TinyDB(DATABASE_FILE)
        self.tables = {}

    @plugin.hookimpl
    def close(self):
        self.db.close()

    @plugin.hookimpl
    def create_tables(self, plugins):
        self.tables = {p: self.db.table(type(p).__name__.lower()) for p in plugins}
        self.tables['post'] = self.db.table('post')

    @plugin.hookimpl
    def insert_post(self, post, plugins):
        post_dict = vars(post)
        post_dict = {k: post_dict[k] for k in POST_FIELDS}
        post_dict['subreddit'] = post.subreddit.display_name
        self.tables['post'].insert(post_dict)

        for p in plugins:
            self.tables[p].insert({'id': post.id})

    @plugin.hookimpl
    def select_posts(self):
        return self.tables['post'].all()
