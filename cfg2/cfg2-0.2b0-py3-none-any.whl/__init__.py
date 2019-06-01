try:
    from .__version__ import VERSION
except:               # pragma: no cover
    VERSION='unknown'
from ._logging import logger as log
from .data import Proxy
from .file import ConfigFile
__all__ = []
