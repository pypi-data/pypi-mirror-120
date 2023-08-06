import os
from importlib import import_module

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.settings'))

def connect(**kwargs):
    raise NotImplementedError()