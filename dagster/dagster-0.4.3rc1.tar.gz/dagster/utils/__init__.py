# For some reason pylint is not finding the Mapping class
from collections import Mapping  # pylint: disable=no-name-in-module
import contextlib
import errno
import inspect
import os
import re
import yaml
import multiprocessing

from dagster import check

from .yaml_utils import load_yaml_from_path, load_yaml_from_globs, load_yaml_from_glob_list


def script_relative_path(file_path):
    '''
    Useful for testing with local files. Use a path relative to where the
    test resides and this function will return the absolute path
    of that file. Otherwise it will be relative to script that
    ran the test
    '''
    # from http://bit.ly/2snyC6s

    check.str_param(file_path, 'file_path')
    scriptdir = inspect.stack()[1][1]
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(scriptdir)), file_path))


# Adapted from https://github.com/okunishinishi/python-stringcase/blob/master/stringcase.py
def camelcase(string):
    check.str_param(string, 'string')

    string = re.sub(r'^[\-_\.]', '', str(string))
    if not string:
        return string
    return str(string[0]).upper() + re.sub(
        r'[\-_\.\s]([a-z])', lambda matched: str(matched.group(1)).upper(), string[1:]
    )


def single_item(ddict):
    check.dict_param(ddict, 'ddict')
    check.param_invariant(len(ddict) == 1, 'ddict')
    return list(ddict.items())[0]


@contextlib.contextmanager
def pushd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(old_cwd)


def safe_isfile(path):
    '''"Backport of Python 3.8 os.path.isfile behavior.

    This is intended to backport https://docs.python.org/dev/whatsnew/3.8.html#os-path. I'm not
    sure that there are other ways to provoke this behavior on Unix other than the null byte,
    but there are certainly other ways to do it on Windows. Afaict, we won't mask other
    ValueErrors, and the behavior in the status quo ante is rough because we risk throwing an
    unexpected, uncaught ValueError from very deep in our logic.
    '''
    try:
        return os.path.isfile(path)
    except (ValueError):
        return False


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def merge_dicts(left, right):
    check.dict_param(left, 'left')
    check.dict_param(right, 'right')

    result = left.copy()
    result.update(right)
    return result


class frozendict(dict):
    def __readonly__(self, *args, **kwargs):
        raise RuntimeError("Cannot modify ReadOnlyDict")

    # https://docs.python.org/3/library/pickle.html#object.__reduce__
    #
    # For a dict, the default behavior for pickle is to iteratively call __setitem__ (see 5th item in __reduce__ tuple).
    # Since we want to disable __setitem__ and still inherit dict, we override this behavior by defining __reduce__.
    # We return the 3rd item in the tuple, which is passed to __setstate__ allowing us to restore the frozendict.

    def __reduce__(self):
        return (frozendict, (), dict(self))

    def __setstate__(self, state):
        self.__init__(state)

    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__
    del __readonly__


class frozenlist(list):
    def __readonly__(self, *args, **kwargs):
        raise RuntimeError("Cannot modify ReadOnlyList")

    __setitem__ = __readonly__
    __delitem__ = __readonly__
    append = __readonly__
    clear = __readonly__
    extend = __readonly__
    insert = __readonly__
    pop = __readonly__
    remove = __readonly__
    reverse = __readonly__
    sort = __readonly__


def make_readonly_value(value):
    if isinstance(value, list):
        return frozenlist(list(map(make_readonly_value, value)))
    elif isinstance(value, dict):
        return frozendict({key: make_readonly_value(value) for key, value in value.items()})
    else:
        return value


def get_prop_or_key(elem, key):
    if isinstance(elem, Mapping):
        return elem.get(key)
    else:
        return getattr(elem, key)


def list_pull(alist, key):
    return list(map(lambda elem: get_prop_or_key(elem, key), alist))


def get_multiprocessing_context():
    # Set execution method to spawn, to avoid fork and to have same behavior between platforms.
    # Older versions are stuck with whatever is the default on their platform (fork on
    # Unix-like and spawn on windows)
    #
    # https://docs.python.org/3/library/multiprocessing.html#multiprocessing.get_context
    if hasattr(multiprocessing, 'get_context'):
        return multiprocessing.get_context('spawn')
    else:
        return multiprocessing
