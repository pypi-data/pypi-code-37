from enti.settings import Config
from pprint import pformat
from textwrap import wrap
from shutil import get_terminal_size

_tw = _terminal_width = get_terminal_size((100,100))[0]

def debug(message=None, depth=1, data=None):
    if Config.DEBUG_ENABLED and depth <= Config.DEBUG_LEVEL:
        indent = 4*depth
        if message is not None:
            lines = wrap(message, width=_tw-indent,
                         initial_indent=" " * indent,
                         subsequent_indent=" " * indent)
            print('\n'.join(lines))
        if data is not None:
            _indent = 4 * (depth + 1)
            if isinstance(data, str):
                lines = wrap(data, width=_tw-_indent,
                             initial_indent=" "*_indent,
                             subsequent_indent=" "*_indent)
                print('\n'.join(lines))
            else:
                lines = pformat(data, width=_tw - _indent, compact=True).split("\n")
                lines = [" "*_indent+l for l in lines]
                print('\n'.join(lines))



