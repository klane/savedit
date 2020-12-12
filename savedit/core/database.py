from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

DATABASE_FILE = 'savedit.db'
DB = SqliteDatabase(DATABASE_FILE)


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
