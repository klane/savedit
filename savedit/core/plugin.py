import importlib
import inspect
import pkgutil
from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple

from savedit import plugins
from savedit.core.database import DB, Post, get_plugin_table

PLUGINS = {}
FAILED_PLUGINS = set()
PluginProps = namedtuple('PluginProps', ['type', 'cls'])


def import_plugins():
    plugin_path, plugin_name = plugins.__path__, plugins.__name__ + '.'

    for _, name, _ in pkgutil.iter_modules(plugin_path, plugin_name):
        try:
            importlib.import_module(name)
        except ModuleNotFoundError:
            FAILED_PLUGINS.add(name)


def load_plugins(selected_plugins):
    if len(PLUGINS) == 0:
        import_plugins()

    plugins = defaultdict(list)

    for p in selected_plugins:
        if p not in PLUGINS:
            raise PluginNotFoundError(p)

        plugins[PLUGINS[p].type].append(PLUGINS[p].cls())

    for p in plugins['service']:
        p.table = get_plugin_table(p)

    tables = [p.table for p in plugins['service']] + [Post]
    DB.create_tables(tables)

    return plugins


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
            plugin_name = cls.__name__.lower()
            plugin_type = cls.__base__.__name__.lower()
            PLUGINS[plugin_name] = PluginProps(type=plugin_type, cls=cls)

    def __repr__(self):
        return type(self).__name__


class Notification(Plugin):
    @abstractmethod
    def notify(self, post, services):
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

    def save_post(self, post):
        self._save_post(post)
        self.table.create(post=post)
