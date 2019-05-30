from ._version import version_info, __version__

from .endpoint import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'acoewidgets',
        'require': 'acoewidgets/extension'
    }]
