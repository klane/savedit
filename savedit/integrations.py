from abc import ABC, abstractmethod


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
