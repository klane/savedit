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


class Plugin:
    @property
    def table(self):
        class Table(BaseModel):
            post = ForeignKeyField(Post)

            class Meta:
                table_name = self.table_name

        return Table

    @property
    def table_name(self):
        return type(self).__name__.lower()
