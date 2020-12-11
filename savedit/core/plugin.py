import importlib
import inspect
import pkgutil
from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple

from savedit import plugins

from .database import Plugin as PluginTable

PLUGINS = {}
PluginProps = namedtuple('PluginSpec', ['type', 'cls'])


def import_plugins():
    plugin_path, plugin_name = plugins.__path__, plugins.__name__ + '.'

    for _, name, _ in pkgutil.iter_modules(plugin_path, plugin_name):
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            pass


def select_plugins(selected_plugins):
    plugins = defaultdict(list)

    for p in selected_plugins:
        plugins[PLUGINS[p].type].append(PLUGINS[p].cls())

    return plugins


class Plugin(ABC):
    def __init_subclass__(cls):
        if not inspect.isabstract(cls):
            plugin_name = cls.__name__.lower()
            plugin_type = cls.__base__.__name__.lower()
            PLUGINS[plugin_name] = PluginProps(type=plugin_type, cls=cls)

    def __repr__(self):
        return type(self).__name__

    @classmethod
    def get_registered(cls):
        return [c() for c in cls.__subclasses__() if c.is_registered()]

    @staticmethod
    @abstractmethod
    def is_registered():
        pass


class Notification(Plugin):
    @abstractmethod
    def notify(self, post, services):
        pass


class Service(Plugin, PluginTable):
    @staticmethod
    @abstractmethod
    def check_post(post):
        pass

    @abstractmethod
    def is_saved(self, post):
        pass

    @abstractmethod
    def _save_post(self, post):
        pass

    def save_post(self, post):
        self._save_post(post)
        self.table.create(post=post)
