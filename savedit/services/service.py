from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def is_saved(self, post):
        pass

    @abstractmethod
    def save_post(self, post):
        pass
