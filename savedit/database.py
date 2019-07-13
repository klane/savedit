from peewee import BooleanField, CharField, IntegerField, Model, SqliteDatabase

DATABASE_FILE = '../savedit.db'
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


TABLES = [Post]
