from abc import ABC, abstractmethod


class Notification(ABC):
    @staticmethod
    @abstractmethod
    def is_registered():
        pass

    @abstractmethod
    def notify(self, post):
        pass
