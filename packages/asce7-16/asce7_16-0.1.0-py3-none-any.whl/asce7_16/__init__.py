import importlib.resources

__version__ = importlib.resources.read_text(__name__, '__version__')

from . import seismic
