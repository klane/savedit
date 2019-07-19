from abc import ABC, abstractmethod

from .database import Integration as IntegrationTable


class Integration(ABC):
    @classmethod
    def get_registered(cls):
        return [c() for c in cls.__subclasses__() if c.is_registered()]

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

    @abstractmethod
    def save_post(self, post):
        pass

    @property
    def table_name(self):
        return self.__name__.lower()

    @property
    def table(self):
        class Table(IntegrationTable):
            class Meta:
                table_name = self.table_name

        return Table
