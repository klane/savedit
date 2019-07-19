from abc import ABC, abstractmethod

from .database import Integration as IntegrationTable


class Integration(ABC):
    @classmethod
    def get_registered(cls):
        return [c for c in cls.__subclasses__() if c.is_registered()]

    @staticmethod
    @abstractmethod
    def is_registered():
        pass


class Notification(Integration):
    @abstractmethod
    def notify(self, post):
        pass


class Service(Integration):
    @staticmethod
    @abstractmethod
    def check_post(post):
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
        class Table(IntegrationTable):
            class Meta:
                table_name = cls.name().lower()

        return Table
