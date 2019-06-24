import sqlite3

from .service import Service


class DatabaseService(Service):
    def __init__(self, file):
        self.table_name = 'POSTS'
        self.conn = sqlite3.connect(file)

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def create(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS {} (
            ID TEXT,
            UTC INTEGER,
            TITLE TEXT,
            IS_SELF INTEGER,
            SELF_TEXT TEXT,
            PERMALINK TEXT,
            URL TEXT,
            SUBREDDIT TEXT
        )""".format(self.table_name))

    def is_saved(self, post):
        pass

    def reset(self):
        self.conn.execute('DROP TABLE IF EXISTS ' + self.table_name)
        self.conn.execute('VACUUM')
        self.create()

    def save_post(self, post):
        row = (
            post.id,
            post.created_utc,
            post.title,
            post.is_self,
            post.selftext,
            post.permalink,
            post.url,
            post.subreddit.display_name
        )

        self.conn.execute(
            "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?)".format(self.table_name), row)
