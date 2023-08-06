__version__ = "0.1.2"
__author__ = 'Imtiaz Mangerah'

import importlib
import inspect
import sys
from collections.abc import MutableMapping, Mapping
from dataclasses import dataclass, field
from pkgutil import iter_modules
from types import SimpleNamespace
from typing import Dict, List, NamedTuple, Union, Optional, Callable


# CaseInsensitiveDict from `requests.structures`
class CaseInsensitiveDict(MutableMapping):
    """
    A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive:

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.
    """

    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, dict(self.items()))


class Request(NamedTuple):
    body: dict
    headers: CaseInsensitiveDict = None
    cookies: SimpleNamespace = None
    context: SimpleNamespace = None

@dataclass
class Response:
    status: int = 500
    body: Optional[Union[Dict, List, str, int, float]] = None
    headers: CaseInsensitiveDict = field(default_factory=CaseInsensitiveDict)
    context: SimpleNamespace = field(default_factory=SimpleNamespace)


class RpcCall(NamedTuple):
    controller: str
    method: str
    args: List
    kwargs: Dict


class Controller:
    _register = {}
    _modules = set()
    Response = Response

    @classmethod
    def __init_subclass__(cls, **kwargs):
        controller_name = cls.__name__
        if controller_name in cls._register:
            raise RuntimeError(f"Duplicate controller registered: {controller_name}")

        super().__init_subclass__(**kwargs)
        cls._register[controller_name] = cls

    @classmethod
    def register(cls, controller_name: str, method: Callable):
        """
        Explicit registration of a method to a controller. Will create an instance of SimpleNamespace to hold
        the controllers methods
        """
        if controller_name in cls._register and inspect.isclass(cls._register[controller_name]):
            if issubclass(cls._register[controller_name], Controller):
                raise RuntimeError("A class based controller cannot register methods using Controller.register")

        controller = cls._register[controller_name] if controller_name in cls._register else SimpleNamespace()

        if hasattr(controller, method.__name__):
            raise RuntimeError(f"Duplicate method {method.__name__} registered  for controller {controller_name}")

        setattr(controller, method.__name__, method)
        cls._register[controller_name] = controller

    @classmethod
    def get_method(cls, controller, method):
        return getattr(cls._register[controller], method)

    @classmethod
    def reset(cls):
        """
        This is used to remove all controllers from the register and delete the modules that was imported such that
        importing the controllers again will re-register them. This is mainly useful for testing when the imports need
        to be reset for each test case. Without the reset, since the module containing the controllers was previously
        imported, the `__init_subclass__` of Controllers will not run, and neither will the rpc_function decorator.
        """
        cls._register = {}
        for module in cls._modules:
            if module.__name__ in sys.modules:
                del sys.modules[module.__name__]

        cls._modules.clear()

class Urn:

    def __init__(self):
        """
        Plugin architecture inspired by bottle.py
        """
        self.plugins = []
        self.skip_plugins = []

    def install(self, plugin):
        """ Add a plugin to the list of plugins and prepare it for being
            applied to all routes of this application. A plugin may be a simple
            decorator or an object that implements the :class:`Plugin` API.
        """
        if hasattr(plugin, 'setup'): plugin.setup(self)
        if not callable(plugin) and not hasattr(plugin, 'apply'):
            raise TypeError("Plugins must be callable or implement .apply()")
        self.plugins.append(plugin)
        self.reset()
        return plugin

    def uninstall(self, plugin):
        """ Uninstall plugins. Pass an instance to remove a specific plugin, a type
            object to remove all plugins that match that type, a string to remove
            all plugins with a matching ``name`` attribute or ``True`` to remove all
            plugins. Return the list of removed plugins. """
        removed, remove = [], plugin
        for i, plugin in list(enumerate(self.plugins))[::-1]:
            if remove is True or remove is plugin or remove is type(plugin) \
                    or getattr(plugin, 'name', True) == remove:
                removed.append(plugin)
                del self.plugins[i]
                if hasattr(plugin, 'close'): plugin.close()
        if removed: self.reset()
        return removed

    def reset(self):
        ...

    def close(self):
        """ Close the application and all installed plugins. """
        for plugin in self.plugins:
            if hasattr(plugin, 'close'): plugin.close()

    def _apply_plugins(self, rpc):
        skiplist = self.skip_plugins + rpc._config.skip_plugins
        for plugin in self.all_plugins(rpc_plugins=rpc._config.plugins, skiplist=skiplist):
            config = rpc._config
            if hasattr(plugin, 'apply'):
                rpc = plugin.apply(rpc)
            else:
                rpc = plugin(rpc)
            rpc._config = config
        return rpc

    def all_plugins(self, rpc_plugins: List, skiplist: List):
        """ Yield all Plugins. """
        unique = set()
        for p in reversed(self.plugins + rpc_plugins):
            if True in skiplist: break
            name = getattr(p, 'name', False)
            if name and (name in skiplist or name in unique): continue
            if p in skiplist or type(p) in skiplist: continue
            if name: unique.add(name)
            yield p

    @staticmethod
    def parse(body: dict) -> RpcCall:
        controller: str = body.get("controller")
        method: str = body.get("method")
        args: List = body.get("args", [])
        kwargs: Dict = body.get("kwargs", {})

        # Ensure all params are of expected types
        assert isinstance(controller, str)
        assert isinstance(method, str)
        assert isinstance(args, List)
        assert isinstance(kwargs, Dict)

        # Ensure controller and method is valid python identifiers
        assert controller.isidentifier()
        assert method.isidentifier()

        return RpcCall(controller, method, args, kwargs)

    @staticmethod
    def import_controllers(controller_module_name):
        controller_module = importlib.import_module(controller_module_name)
        modules = {controller_module}
        for controller in iter_modules(controller_module.__path__):
            modules.add(importlib.import_module(f"{controller_module_name}.{controller.name}"))

        Controller._modules.update(modules)

    def execute(self, body, headers=None, context=None):
        context, cookies = SimpleNamespace(**(context or {})), SimpleNamespace()

        try:
            call = self.parse(body)
        except AssertionError:
            return Response(status=400, body="Bad Request. Unable to parse RPC Call.")

        request = Request(body=body, headers=CaseInsensitiveDict(headers), context=context, cookies=cookies)

        try:
            method = Controller.get_method(call.controller, call.method)
        except KeyError:
            return Response(status=400, body=f"Controller {call.controller} was not found")
        except AttributeError:
            return Response(status=400, body=f"Method {call.method} of Controller {call.controller} was not found")

        if not hasattr(method, '_config') or method._config.callable == False:
            return Response(status=400, body=f"Method {call.method} of Controller {call.controller} is not callable.")

        return self._apply_plugins(method)(request, *call.args, **call.kwargs)


def makelist(data):
    if isinstance(data, (tuple, list, set, dict)):
        return list(data)
    elif data:
        return [data]
    else:
        return []

def add_config_to_method(func, plugins=None, skip_plugins=None, **config):
    if not hasattr(func, '_config'):
        func._config = SimpleNamespace(**config)

    func._config.callable = True
    func._config.plugins = makelist(plugins)
    func._config.skip_plugins = makelist(skip_plugins)

    return func

def rpc(plugins=None, skip_plugins=None, **config):
    def rpc_wrapper(func):
        return add_config_to_method(func, plugins, skip_plugins, **config)
    return rpc_wrapper

def rpc_function(plugins=None, skip_plugins=None, **config):
    def rpc_wrapper(func):
        controller_name = func.__module__.rpartition('.')[2]
        Controller.register(controller_name, func)
        return add_config_to_method(func, plugins, skip_plugins, **config)

    return rpc_wrapper