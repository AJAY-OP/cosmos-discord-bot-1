from .core import Cosmos
from .core import utilities
from .core.functions import exceptions


__release__ = "Babu"
__version__ = "0.2.0"


def get_bot():
    return Cosmos(version=__version__, release=__release__)
