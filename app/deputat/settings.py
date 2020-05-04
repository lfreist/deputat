import os

def base_dir():
    return os.getcwd()

def icon_dir():
    return os.path.join(base_dir(), 'GUI', 'pictures')