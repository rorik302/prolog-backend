import importlib
import os

from .base import SharedModel, TenantModel

__all__ = ["SharedModel", "TenantModel"]

model_dir = os.path.dirname(__file__)
for file in os.listdir(model_dir):
    if file.endswith(".py") and file != "__init__.py" and file != "base.py":
        module_name = f"{__name__}.{file[:-3]}"
        importlib.import_module(module_name)
