import importlib
import inspect
import pkgutil
from abc import ABC, abstractmethod

import pluggy

from savedit import plugins

PLUGINS = {}
FAILED_PLUGINS = set()
PluginManager = pluggy.PluginManager('savedit')
hookspec = pluggy.HookspecMarker('savedit')
hookimpl = pluggy.HookimplMarker('savedit')


def import_plugins():
    plugin_path, plugin_name = plugins.__path__, plugins.__name__ + '.'

    for _, name, _ in pkgutil.walk_packages(plugin_path, plugin_name):
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            FAILED_PLUGINS.add(name)


def load_plugins(plugins):
    import_plugins()
    services = []

    for p in plugins:
        if p not in PLUGINS:
            raise PluginNotFoundError(p)

        plugin = PLUGINS[p]()
        PluginManager.register(plugin)

        if isinstance(plugin, Service):
            services.append(plugin)

    PluginManager.hook.create_tables(plugins=services)


class PluginNotFoundError(Exception):
    def __init__(self, plugin):
        message = f'Plugin {plugin} not registered'

        if len(PLUGINS) > 0:
            available = '\n'.join(sorted(PLUGINS))
            message += f'\n\nAvailable plugins:\n{available}'
        else:
            message += '. No plugins available.'

        if len(FAILED_PLUGINS) > 0:
            failed = '\n'.join(sorted(FAILED_PLUGINS))
            message += '\n\nThe following modules failed to load.'
            message += f' Check that all dependencies are installed.\n{failed}'

        super().__init__(message)


class Plugin(ABC):
    def __init_subclass__(cls):
        if not inspect.isabstract(cls):
            PLUGINS[cls.__name__.lower()] = cls

    def __repr__(self):
        return type(self).__name__


class Database(Plugin):
    @hookspec
    @abstractmethod
    def close(self):
        pass

    @hookspec
    @abstractmethod
    def create_tables(self, plugins):
        pass

    @hookspec
    @abstractmethod
    def insert_post(self, post, plugins):
        pass

    @hookspec
    @abstractmethod
    def select_posts(self):
        pass


class Notification(Plugin):
    @hookspec
    @abstractmethod
    def notify(self, post, services):
        pass


class Service(Plugin):
    @abstractmethod
    def check_post(self, post):
        pass

    @hookimpl
    def run_service(self, post):
        if self.check_post(post):
            self.save_post(post)
            return self

    @abstractmethod
    def save_post(self, post):
        pass
