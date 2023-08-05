import os
from importlib import import_module

settings = import_module(os.environ['FASTAPI_SETTINGS'])

def connect(**kwargs):
    raise NotImplementedError()