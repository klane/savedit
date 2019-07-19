from abc import ABC, abstractmethod

from peewee import ForeignKeyField

from .database import BaseModel, Post


class Notification(ABC):
    @staticmethod
    @abstractmethod
    def is_registered():
        pass

    @abstractmethod
    def notify(self, post):
        pass


class Service(ABC):
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

    @staticmethod
    @abstractmethod
    def name():
        pass

    @abstractmethod
    def save_post(self, post):
        pass

    @classmethod
    def table(cls):
        class Table(BaseModel):
            post = ForeignKeyField(Post)

            class Meta:
                table_name = cls.name().lower()

        return Table
