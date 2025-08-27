import pkgutil
import importlib
import inspect
from typing import List, Type
from connectors.base_connector import BaseConnector

def load_connector_classes() -> List[Type[BaseConnector]]:
    connector_classes = []
    import connectors
    package_path = connectors.__path__
    for finder, name, ispkg in pkgutil.iter_modules(package_path):
        if name.startswith("__") or name == "base_connector":
            continue
        module = importlib.import_module(f"connectors.{name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            try:
                if issubclass(obj, BaseConnector) and obj is not BaseConnector:
                    connector_classes.append(obj)
            except TypeError:
                continue
    return connector_classes
