from abc import ABC, abstractmethod

from peewee import ForeignKeyField

from ..database import BaseModel, Post


class Service(ABC):
    class Table(BaseModel):
        post = ForeignKeyField(Post)

    @staticmethod
    @abstractmethod
    def check_post(post):
        pass

    @staticmethod
    @abstractmethod
    def is_registered():
        pass

    @abstractmethod
    def is_saved(self, post):
        pass

    @abstractmethod
    def save_post(self, post):
        pass
