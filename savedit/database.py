import pkgutil

from peewee import BooleanField, CharField, ForeignKeyField, IntegerField, Model, SqliteDatabase

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
        super(Post, cls).create(**vars(post))


class Service(BaseModel):
    post = ForeignKeyField(Post)


services = [name for (_, name, _) in pkgutil.iter_modules(['savedit/services'])]
TABLES = [type(name, (Service,), {}) for name in services] + [Post]
