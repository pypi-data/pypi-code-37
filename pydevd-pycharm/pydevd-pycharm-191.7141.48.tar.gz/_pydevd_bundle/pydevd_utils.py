from __future__ import nested_scopes
import traceback
import os

try:
    from urllib import quote
except:
    from urllib.parse import quote  # @UnresolvedImport

try:
    from collections import OrderedDict
except:
    OrderedDict = dict

import inspect
from _pydevd_bundle.pydevd_constants import IS_PY3K, dict_iter_items
import sys
from _pydev_bundle import pydev_log


def save_main_module(file, module_name):
    # patch provided by: Scott Schlesier - when script is run, it does not
    # use globals from pydevd:
    # This will prevent the pydevd script from contaminating the namespace for the script to be debugged
    # pretend pydevd is not the main module, and
    # convince the file to be debugged that it was loaded as main
    sys.modules[module_name] = sys.modules['__main__']
    sys.modules[module_name].__name__ = module_name
    from imp import new_module

    m = new_module('__main__')
    sys.modules['__main__'] = m
    if hasattr(sys.modules[module_name], '__loader__'):
        m.__loader__ = getattr(sys.modules[module_name], '__loader__')
    m.__file__ = file

    return m


def to_number(x):
    if is_string(x):
        try:
            n = float(x)
            return n
        except ValueError:
            pass

        l = x.find('(')
        if l != -1:
            y = x[0:l-1]
            #print y
            try:
                n = float(y)
                return n
            except ValueError:
                pass
    return None


def compare_object_attrs_key(x):
    if '__len__' == x:
        # __len__ should appear after other attributes in a list.
        num = 99999999
    else:
        num = to_number(x)
    if num is not None:
        return 1, num
    else:
        return -1, to_string(x)


if IS_PY3K:
    def is_string(x):
        return isinstance(x, str)

else:
    def is_string(x):
        return isinstance(x, basestring)

def to_string(x):
    if is_string(x):
        return x
    else:
        return str(x)

def print_exc():
    if traceback:
        traceback.print_exc()

if IS_PY3K:
    def quote_smart(s, safe='/'):
        return quote(s, safe)
else:
    def quote_smart(s, safe='/'):
        if isinstance(s, unicode):
            s =  s.encode('utf-8')

        return quote(s, safe)


def get_clsname_for_code(code, frame):
    clsname = None
    if len(code.co_varnames) > 0:
        # We are checking the first argument of the function
        # (`self` or `cls` for methods).
        first_arg_name = code.co_varnames[0]
        if first_arg_name in frame.f_locals:
            first_arg_obj = frame.f_locals[first_arg_name]
            if inspect.isclass(first_arg_obj):  # class method
                first_arg_class = first_arg_obj
            else:  # instance method
                first_arg_class = first_arg_obj.__class__
            func_name = code.co_name
            if hasattr(first_arg_class, func_name):
                method = getattr(first_arg_class, func_name)
                func_code = None
                if hasattr(method, 'func_code'):  # Python2
                    func_code = method.func_code
                elif hasattr(method, '__code__'):  # Python3
                    func_code = method.__code__
                if func_code and func_code == code:
                    clsname = first_arg_class.__name__
    return clsname


def _get_project_roots(project_roots_cache=[]):
    # Note: the project_roots_cache is the same instance among the many calls to the method
    if not project_roots_cache:
        roots = os.getenv('IDE_PROJECT_ROOTS', '').split(os.pathsep)
        pydev_log.debug("IDE_PROJECT_ROOTS %s\n" % roots)
        new_roots = []
        for root in roots:
            new_roots.append(os.path.normcase(root))
        project_roots_cache.append(new_roots)
    return project_roots_cache[-1] # returns the project roots with case normalized


def _get_library_roots(library_roots_cache=[]):
    # Note: the project_roots_cache is the same instance among the many calls to the method
    if not library_roots_cache:
        roots = os.getenv('LIBRARY_ROOTS', '').split(os.pathsep)
        pydev_log.debug("LIBRARY_ROOTS %s\n" % roots)
        new_roots = []
        for root in roots:
            new_roots.append(os.path.normcase(root))
        library_roots_cache.append(new_roots)
    return library_roots_cache[-1] # returns the project roots with case normalized


def not_in_project_roots(filename, filename_to_not_in_scope_cache={}):
    # Note: the filename_to_not_in_scope_cache is the same instance among the many calls to the method
    try:
        return filename_to_not_in_scope_cache[filename]
    except:
        project_roots = _get_project_roots()
        original_filename = filename
        if not os.path.isabs(filename) and not filename.startswith('<'):
            filename = os.path.abspath(filename)
        filename = os.path.normcase(filename)
        for root in project_roots:
            if len(root) > 0 and filename.startswith(root):
                filename_to_not_in_scope_cache[original_filename] = False
                break
        else: # for else (only called if the break wasn't reached).
            filename_to_not_in_scope_cache[original_filename] = True

        if not filename_to_not_in_scope_cache[original_filename]:
            # additional check if interpreter is situated in a project directory
            library_roots = _get_library_roots()
            for root in library_roots:
                if root != '' and filename.startswith(root):
                    filename_to_not_in_scope_cache[original_filename] = True

        # at this point it must be loaded.
        return filename_to_not_in_scope_cache[original_filename]


def is_filter_enabled():
    return os.getenv('PYDEVD_FILTERS') is not None


def is_filter_libraries():
    is_filter = os.getenv('PYDEVD_FILTER_LIBRARIES') is not None
    pydev_log.debug("PYDEVD_FILTER_LIBRARIES %s\n" % is_filter)
    return is_filter


def _get_stepping_filters(filters_cache=[]):
    if not filters_cache:
        filters = os.getenv('PYDEVD_FILTERS', '').split(';')
        pydev_log.debug("PYDEVD_FILTERS %s\n" % filters)
        new_filters = []
        for new_filter in filters:
            new_filters.append(new_filter)
        filters_cache.append(new_filters)
    return filters_cache[-1]


def is_ignored_by_filter(filename, filename_to_ignored_by_filters_cache={}):
    try:
        return filename_to_ignored_by_filters_cache[filename]
    except:
        import fnmatch
        for stepping_filter in _get_stepping_filters():
            if fnmatch.fnmatch(filename, stepping_filter):
                pydev_log.debug("File %s ignored by filter %s" % (filename, stepping_filter))
                filename_to_ignored_by_filters_cache[filename] = True
                break
        else:
            filename_to_ignored_by_filters_cache[filename] = False

        return filename_to_ignored_by_filters_cache[filename]


def take_first_n_coll_elements(coll, n):
    if coll.__class__ in (list, tuple):
        return coll[:n]
    elif coll.__class__ in (set, frozenset):
        buf = []
        for i, x in enumerate(coll):
            if i >= n:
                break
            buf.append(x)
        return type(coll)(buf)
    elif coll.__class__ in (dict, OrderedDict):
        ret = type(coll)()
        for i, (k, v) in enumerate(dict_iter_items(coll)):
            if i >= n:
                break
            ret[k] = v
        return ret
    else:
        raise TypeError("Unsupported collection type: '%s'" % str(coll.__class__))


class VariableWithOffset(object):
    def __init__(self, data, offset):
        self.data, self.offset = data, offset


def get_var_and_offset(var):
    if isinstance(var, VariableWithOffset):
        return var.data, var.offset
    return var, 0

