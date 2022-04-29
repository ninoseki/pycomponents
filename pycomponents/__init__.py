import importlib.metadata as importlib_metadata

from . import constants

__version__ = importlib_metadata.version(constants.project_name)
