from .base import *   # NOQA
try:
    from .local import *  # NOQA
except ImportError:
    print('Local settings not found')
