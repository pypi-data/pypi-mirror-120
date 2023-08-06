import os

def get_all_env():
    return dict(os.environ)

def set_env(name, value):
    os.environ[name] = value

def get_env(name):
    try:
        return os.environ[name]
    except KeyError:
        return None
