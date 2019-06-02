'''
sinfo finds and prints version information for loaded modules in the current
session, Python, and the OS.
'''

import sys
import types
import platform
import inspect
from datetime import datetime
from multiprocessing import cpu_count

from stdlib_list import stdlib_list


def imports(environ):
    '''Find modules in an environment.'''
    for name, val in environ:
        # If the module was directly imported
        if isinstance(val, types.ModuleType):
            yield val.__name__
        # If something was imported from the module
        else:
            try:
                yield val.__module__.split('.')[0]
            except AttributeError:
                pass


def sinfo(print_na=True, print_os=True, print_cpu=True, print_jupyter=True,
          print_implicit=False, print_std_lib=False, print_private=False,
          write_req_file=True, req_file_name=None,
          excludes=['builtins', 'sinfo', 'stdlib_list']):
    '''
    Print version information for loaded modules in the current session,
    Python, and the OS.

    Parameters
    ----------
    print_na : bool
        Print module name even when no version number is found.
    print_os : bool
        Print OS information.
    print_cpu : bool
        Print number of logical CPU cores and info string (if available).
    print_jupyter : bool
        Print information about the jupyter environment if called from a
        notebook.
    print_implicit : bool
        Print information about modules imported by the Python interpreter on
        startup and depency modules imported via other modules. This is often
        rather verbose and setting `print_na` to `False` is recommended.
    print_std_lib : bool
        Print information for modules imported from the standard library.
    print_private : bool
        Print information for private modules.
    excludes : list
        Do not print version information for these modules.
    '''
    # Exclude std lib packages
    if not print_std_lib:
        try:
            std_modules = stdlib_list(version=platform.python_version()[:-2])
        except ValueError:
            # Use the latest available if the Python version cannot be found
            std_modules = stdlib_list('3.7')
        excludes = excludes + std_modules
    # Get `globals()` from the enviroment where the function is executed
    caller_globals = dict(
        inspect.getmembers(inspect.stack()[1][0]))["f_globals"]
    # Find imported modules in the global namespace
    imported_modules = set(imports(caller_globals.items()))
    # If running in the notebook, print IPython with the other notebook modules
    if 'jupyter_core' in sys.modules.keys() and 'IPython' in imported_modules:
        imported_modules.remove('IPython')
    # Include all modules from sys.modules
    if print_implicit:
        sys_modules = set(sys.modules.keys())
        imported_modules = imported_modules.union(sys_modules)
    # Keep module basename only. Filter duplicates and excluded modules.
    if print_private:
        clean_modules = set(module.split('.')[0] for module in imported_modules
                            if module.split('.')[0] not in excludes)
    else:
        clean_modules = set(module.split('.')[0] for module in imported_modules
                            if module.split('.')[0] not in excludes
                            and not module.startswith('_'))
    # Find version number. Return NA if a version string can't be found.
    # This section is originally from `py_session` and modified slightly
    mod_and_ver = []
    for module in clean_modules:
        try:
            mod_and_ver.extend([
                f'{module:10}\t{sys.modules[module].__version__}'])
        except AttributeError:
            try:
                if (isinstance(sys.modules[module].version, str)
                        or isinstance(sys.modules[module].version, int)):
                    mod_and_ver.extend([
                        f'{module:10}\t{sys.modules[module].version}'])
                else:
                    mod_and_ver.extend([
                        f'{module:10}\t{sys.modules[module].version()}'])
            except AttributeError:
                try:
                    mod_and_ver.extend([
                        f'{module:10}\t{sys.modules[module].VERSION}'])
                except AttributeError:
                    if print_na:
                        mod_and_ver.extend([f'{module:10}\tNA'])
    mod_and_ver = sorted(mod_and_ver)
    if mod_and_ver != []:
        print('-----')
        print('\n'.join(mod_and_ver))
    # Print jupyter info separetely if running in the notebook
    if print_jupyter and 'jupyter_core' in sys.modules.keys():
        jup_modules = [sys.modules['IPython'], sys.modules['jupyter_client'],
                       sys.modules['jupyter_core']]
        try:
            import jupyterlab
            jup_modules.append(jupyterlab)
        except ModuleNotFoundError:
            pass
        try:
            import notebook
            jup_modules.append(notebook)
        except ModuleNotFoundError:
            pass
        jup_mod_and_ver = [f'{module.__name__:10}\t{module.__version__}'
                           for module in jup_modules]
        print('-----')
        print('\n'.join(jup_mod_and_ver))
    if write_req_file:
        if req_file_name is None:
            req_file_name = 'sinfo-requirements.txt'
        # Include jupyter modules if the variable is defined
        try:
            mods_to_req = [mod.replace(' ', '').replace('\t', '==')
                           for mod in jup_mod_and_ver + mod_and_ver]
        except NameError:
            mods_to_req = [mod.replace(' ', '').replace('\t', '==')
                           for mod in mod_and_ver]
        with open(req_file_name, 'w') as f:
            for mod_to_req in mods_to_req:
                f.write('{}\n'.format(mod_to_req))
    print('-----')
    print('Python ' + sys.version.replace('\n', ''))
    if print_os:
        print(platform.platform())
    if print_cpu:
        if platform.processor() != '':
            print(f'{cpu_count()} logical CPU cores, {platform.processor()}')
        else:
            print(f'{cpu_count()} logical CPU cores')
    print('-----')
    print('Session information updated at {}'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M')))
