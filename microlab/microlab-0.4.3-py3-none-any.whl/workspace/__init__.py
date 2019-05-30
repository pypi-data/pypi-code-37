from microlab.io.yaml import create_yaml, read_yaml
from microlab.io.files import delete_file, file_exist
from microlab.io.folders import create_folder, folder_exist
from microlab import __version__

import os
import sys

debug = False
memory = {
        'path': None,
        'examples': None,
        }
colors = {'green': "\033[0;32m",
          'blue': "\033[0;34m",
          'default': "\033[0m"}
def usage():
    print('\n {}New Workspace {}'.format(colors['blue'], colors['default']))
    print(' {}workspace_create{}                create new workspace in current directory'.format(colors['green'], colors['default']))

    print('\n {}New Package {}'.format(colors['blue'], colors['default']))
    print(' {}package_create{}                  create new package in current directory'.format(colors['green'], colors['default']))

    print('\n {}Actions for Workspace{}'.format(colors['blue'], colors['default']))
    print(' {}workspace_status{}                view the status of the current workspace'.format(colors['green'], colors['default']))
    print(' {}workspace_rename{}                change the name of the current workspace'.format(colors['green'], colors['default']))
    print(' {}workspace_reversion{}             change the version of the current workspace'.format(colors['green'], colors['default']))
    print(' {}workspace_packages{}              view the packages of the current workspace'.format(colors['green'], colors['default']))
    print(' {}workspace_save{}                  save the workspace yaml file on the current workspace'.format(colors['green'], colors['default']))
    print(' {}workspace_tests{}                 view the tests of the current workspace'.format(colors['green'], colors['default']))

    print('\n {}Actions for Packages {}'.format(colors['blue'], colors['default']))
    print(' {}package_start{}  <package>        start the package of the current workspace'.format(colors['green'], colors['default']))

    print('\n {}Actions for Tests{}'.format(colors['blue'], colors['default']))
    print(' {}test_start{}  <test>              start the test of the current workspace'.format(colors['green'], colors['default']))


# wake up
if sys.platform == 'linux':
    memory['path'] = "/".join(os.path.abspath(__file__).split("/")[:-2])
else:
    memory['path'] = "\\".join(os.path.abspath(__file__).split("\\")[:-2])

memory['examples'] = os.path.join(memory['path'], 'examples')
microlab_tests = {
        'monitoring': os.path.join(memory['examples'], 'hardware', 'monitoring.py'),

        'file': os.path.join(memory['examples'], 'io', 'file_C.R.U.D.py'),
        'json': os.path.join(memory['examples'], 'io', 'json_C.R.U.D.py'),
        'csv': os.path.join(memory['examples'], 'io', 'csv_C.R.U.D.py'),
        'yaml': os.path.join(memory['examples'], 'io', 'yaml_C.R.U.D.py'),
        'zip': os.path.join(memory['examples'], 'io', 'zip_C.R.U.D.py'),

        'signal 1-D': os.path.join(memory['examples'], 'signals', '1d.py'),
        'signal 2-D': os.path.join(memory['examples'], 'signals', '2d.py'),

        'interpolation': os.path.join(memory['examples'], 'methods', 'interpolation.py'),
        'intersection': os.path.join(memory['examples'], 'methods', 'Intersection.py'),

        'symetric': os.path.join(memory['examples'], 'cryptography', 'symmetric.py'),
        'asymetric': os.path.join(memory['examples'], 'cryptography', 'asymmetric.py'),
        }
def help(target):
    print(' - - - - - - - - - - - - -')
    print('  Microlab  v {} '.format(__version__))
    print(' - - - - - - - - - - - - -')

    if target in ['workspace']:
        print('\n load() ')
        print(' save_workspace() ')
        print(' delete() ')

        print('\n change_name( < new name > ) ')
        print(' change_version( < new version >)')

        print('\n status() ')
        print(' show( < test > or < test name >  ,  < packages > or < package name >) ')

        print('\n add_test() ')
        print('\n start( < tests >  or  < test name > ) ')

    elif target in ['packages']:
        print('\n start(  < packages > or < package name > ) ')

    else:
        print('\n target {} is not valid'.format(target))



''' Workspace '''
workspace = {'name': 'workspace',
            'version': '0.1',
            'path': os.getcwd(),
            'tests': {},
            'packages': {}
            }
is_loaded = False
def workspace_create(name):
    """
            Create a workspace folder and sub folders and also the yaml file
    :param name:
    :return:
    """
    if is_loaded:
        print('you are already in a workspace')
    else:
        _workspace = os.path.join(os.getcwd(), name)
        _src = os.path.join(_workspace, 'src')
        _scripts = os.path.join(_workspace, 'scripts')
        _tests = os.path.join(_workspace, 'tests')
        _file = os.path.join(_workspace, 'workspace')

        if not folder_exist(path=_workspace, verbose=False):
            create_folder(path=_workspace, verbose=True)
            create_folder(path=_src, verbose=True)
            create_folder(path=_scripts, verbose=True)
            create_folder(path=_tests, verbose=True)
            workspace_rename(name=name, on_memory=True)
            create_yaml(path=_file, data={'workspace': workspace}, verbose=True)
            print('[ {} ]  created'.format(workspace['name']))
        else:
            print('[ {} ]  folder exist'.format(name))
def workspace_load():
    """
            Load the workspace from yaml file
    :return:
    """
    global workspace, is_loaded

    try:
        # auto fix workspace directory
        workspace_file = read_yaml(path='workspace', verbose=False)
        if workspace_file['workspace']['path'] != os.getcwd():
            print('fixing workspace directory')
            workspace_file['workspace']['path'] = os.getcwd()
            create_yaml(path='workspace', data=workspace_file, verbose=True)
        # reload the warkspace
        workspace_file = read_yaml(path='workspace', verbose=False)
        workspace = workspace_file['workspace']
        workspace['packages'] = load_packages(verbose=False)
        is_loaded = True
        if debug:
            print('[ {} ]   workspace loaded'.format(workspace['name']))
            print('[ {} ]   memory loaded'.format(workspace['name']))

    except Exception as e:
        is_loaded = False
        if debug:
            print('[ {} ]   no workspace found in {}'.format(workspace['name'], os.getcwd()))
            print('[ exception] {}'.format(e))
def workspace_clean():
    """
            Clean the workspace yaml file
    :return:
    """
    workspace['tests'] = {}
    workspace['packages'] = {}
    delete_file(path='workspace', verbose=False)
def workspace_status():
    """
            show the status of the workspace
    :return:
    """
    if is_loaded:
        print('[ {} ]  workspace    {}'.format(workspace['name'], workspace['path']))
        print('[ {} ]  version      {}'.format(workspace['name'], workspace['version']))
        print('[ {} ]  packages     {}'.format(workspace['name'], workspace['packages'].keys().__len__()))
        print('[ {} ]  tests        {}'.format(workspace['name'], workspace['tests'].keys().__len__()))
    else:
        print('this directory is not a workspace{}'.format(workspace['path']))
def workspace_rename(name, on_memory=False):
    """
            Rename the workspace
    :param name:
    :param on_memory:
    :return:
    """
    workspace['name'] = name
    if not on_memory:
        workspace_save()
        workspace_load()
def workspace_reversion(new_version):
    """
                change the version of the workspace
    :param version:
    :return:
    """
    workspace['version'] = new_version
    workspace_save()
    workspace_load()
def workspace_packages():
    """
            Show all packages in workspace
    :return:
    """
    for package_name, package in workspace['packages'].items():
        print('[  {}  ]  '.format(package_name))
        for field, value in package.items():
            print('     {} : {}'.format(field, value))
def workspace_save():
    '''??? '''
    create_yaml(path='workspace',
                data={'workspace': workspace},
                verbose=False)


''' Packages '''
package = {
            'name': 'package',
            'arguments': '',
            'directory': '',
            'executor': '',
            'installer': '',
            'uninstaller': '',
          }
def package_create(package):
    """
                Create a package while you are inside of the workspace
    :param package:
    :return:
    """
    if is_loaded:
        _workspace = os.path.join(os.getcwd())
        _src = os.path.join(_workspace, 'src')
        _scripts = os.path.join(_workspace, 'scripts')
        _tests = os.path.join(_workspace, 'tests')
        _file = os.path.join(_workspace, 'workspace')

        _package = os.path.join(_src, package['name'])
        _package_src = os.path.join(_package, 'src')
        _package_scripts = os.path.join(_package, 'scripts')
        _package_tests = os.path.join(_package, 'tests')
        _package_file = os.path.join(_package, 'package')

        if not folder_exist(path=_package, verbose=False):
            create_folder(path=_package, verbose=True)
            create_folder(path=_package_src, verbose=True)
            create_folder(path=_package_scripts, verbose=True)
            create_folder(path=_package_tests, verbose=True)
            # change_name(name=name, on_memory=True)
            package['directory'] = _package
            create_yaml(path=_package_file, data={'package': package}, verbose=True)

            # workspace['packages'][package['name']] = package
            # create_yaml(path=_file, data={'workspace': workspace}, verbose=True)

            print('[ {} ]  package {} created'.format(workspace['name'], package['name']))
        else:
            print('[ {} ]  folder exist {}'.format(package['name'], _package))

    else:
        print('you are not in the directory of a workspace')
def load_packages(verbose=False):
    """
                Load all packages in workspace src folder
    :param verbose:
    :return:
    """
    _src = os.path.join(workspace['path'], 'src')
    if verbose:
        print('loading packages in {}'.format(_src))
    pkgs = {}
    if folder_exist(path=_src, verbose=False):
        if verbose:
            print('Packages: {}'.format(_src))
        for package_name in os.listdir(_src):
            _package = os.path.join(_src, package_name)
            _package_file = os.path.join(_package, 'package')

            if verbose:
                print('[ {} ] package {} found'.format(workspace['name'], package_name))
            try:

                temp = read_yaml(path=_package_file, verbose=False)

                # auto fix the directory of each package
                if temp['package']['directory'] != _package:
                    temp['package']['directory'] = _package
                    create_yaml(data=temp, path=_package_file)

                # load the package
                pkgs[package_name] = read_yaml(path=_package_file, verbose=False)['package']
            except:
                print('[ {} ] description damaged on package {}'.format(workspace['name'], package_name))
    return pkgs
def package_directory(package_name):
    """
    :param package_name:
    :return: the full path of the package
    """
    return os.path.join(workspace['path'], 'src', package_name)
def package_start(arg):
    if arg in workspace['packages']:
        package_name = arg
        package = workspace['packages'][package_name]
        print(package)
        print('[  {}  ]     is starting'.format(package_name))
        if sys.platform == 'linux':
            full_path = os.path.join(package['directory'], package['executor'])
            command = 'python3 {} {}'.format(full_path, package['arguments'])
        else:
            os.chdir(package['directory'])
            command = 'python {} {}'.format(package['executor'], package['arguments'])
        print('[  {}  ]     COMMAND: {}'.format(package_name, command))
        os.system(command)
def package_add(name, directory, executor, arguments='', installer='install.sh', uninstaller='uninstall.sh'):
    """
                Add new package to workspace

    :param name:
    :param directory:
    :param executor:
    :param arguments:
    :param installer:
    :param uninstaller:
    :return:
    """
    _package = {
                'name': name,
                'arguments': arguments,
                'directory': directory,
                'executor': executor,
                'installer': installer,
                'uninstaller': uninstaller,
              }
    workspace['packages'][name] = _package
    workspace_save()



''' Tests '''
# show workspace tests
def workspace_tests():
    # show all workspace tests
    for test_name, test_path in workspace['tests'].items():
        print('[  {}  ]     {}'.format(test_name, test_path))
# add new test to lab
def add_test(name, directory=None):
    if directory is None:
        if name in microlab_tests:
            workspace['tests'][name] = microlab_tests[name]
    else:
        workspace['test'][name] = directory
    workspace_save()
def test_start(arg):
    if arg in workspace['tests']:
        test_python_scrypt = workspace['tests'][arg]
        if sys.platform == 'linux':
            os.system('python3 {} '.format(test_python_scrypt))
        else:
            os.system('python {} '.format(test_python_scrypt))



''' Microlab '''


def start_microlab_test(arg):
    # start a microlab Test
    if arg in microlab_tests:
        test_python_scrypt = microlab_tests[arg]
        if sys.platform == 'linux':
            os.system('python3 {} '.format(test_python_scrypt))
        else:
            os.system('python {} '.format(test_python_scrypt))


workspace_load()