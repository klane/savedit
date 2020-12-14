from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from savedit.core import Database, plugin

DATABASE_FILE = 'savedit.db'
DB = SqliteDatabase(DATABASE_FILE)


class Sqlite(Database):
    @plugin.hookimpl
    def close(self):
        DB.close()

    @plugin.hookimpl
    def create_tables(self, plugins):
        self.tables = {p: get_plugin_table(p) for p in plugins}
        DB.create_tables(list(self.tables.values()) + [Post])

    @plugin.hookimpl
    def insert_post(self, post, plugins):
        Post.create(post)

        for p in plugins:
            self.tables[p].create(post=post)

    @plugin.hookimpl
    def select_posts(self):
        for post in Post.select():
            yield post.__data__


class BaseModel(Model):
    class Meta:
        database = DB


class Post(BaseModel):
    id = CharField(primary_key=True)
    created_utc = IntegerField()
    title = CharField()
    is_self = BooleanField()
    selftext = CharField()
    permalink = CharField()
    url = CharField()
    subreddit = CharField()

    @classmethod
    def create(cls, post):
        super().create(**vars(post))


def get_plugin_table(plugin):
    class Table(BaseModel):
        post = ForeignKeyField(Post)

        class Meta:
            table_name = type(plugin).__name__.lower()

    return Table
