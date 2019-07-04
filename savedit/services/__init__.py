from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def check_post(self, post):
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
