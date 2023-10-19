"""Internal Utils for the game"""
from pathlib import Path


def module_path():
    """Returns the absolute path of the game module"""
    return Path(__path__[0])
