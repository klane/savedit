import importlib
import inspect
import pkgutil
from abc import ABC, abstractmethod

import pluggy

from savedit import plugins
from savedit.core.database import DB, Post, get_plugin_table

PLUGINS = {}
FAILED_PLUGINS = set()
PluginManager = pluggy.PluginManager('savedit')
hookimpl = pluggy.HookimplMarker('savedit')


def import_plugins():
    plugin_path, plugin_name = plugins.__path__, plugins.__name__ + '.'

    for _, name, _ in pkgutil.iter_modules(plugin_path, plugin_name):
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            FAILED_PLUGINS.add(name)


def load_plugins(plugins):
    import_plugins()
    tables = []

    for p in plugins:
        if p not in PLUGINS:
            raise PluginNotFoundError(p)

        plugin = PLUGINS[p]()
        PluginManager.register(plugin)

        if isinstance(plugin, Service):
            plugin.table = get_plugin_table(plugin)
            tables.append(plugin.table)

    DB.create_tables(tables + [Post])


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


class Notification(Plugin):
    @abstractmethod
    def notify(self, post, service):
        pass


class Service(Plugin):
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

    @hookimpl
    def save_post(self, post):
        if self.check_post(post):
            self._save_post(post)
            self.table.create(post=post)
            PluginManager.hook.notify(post=post, service=self)
