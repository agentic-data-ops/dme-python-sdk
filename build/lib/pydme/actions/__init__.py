# DME Actions 模块

import importlib
import pkgutil
import os

__all__ = []

# Auto-import all action modules so `from pydme.actions import *` works
_actions_path = os.path.dirname(__file__)
for _importer, _modname, _ispkg in pkgutil.iter_modules([_actions_path]):
    if _modname.startswith('_'):
        continue
    _module = importlib.import_module(f'pydme.actions.{_modname}')
    globals()[_modname] = _module
    __all__.append(_modname)
