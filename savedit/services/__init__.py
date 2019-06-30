from abc import ABC, abstractmethod

from .database import DatabaseService


class Service(ABC):
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
