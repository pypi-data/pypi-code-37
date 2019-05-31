import logging
import os
import sys
import pathlib
import poyo
import copy

assert sys.version_info >= (3, 6)

import logging
_logger = logging.getLogger(__name__)

class MandatoryClass():
    pass

MANDATORY = MandatoryClass()

class HaipConfigException(Exception):
    pass

class ConfigContainer(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("Config - No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("Config - No such attribute: " + name)

_config = ConfigContainer()

def load(directory: str, env=None):
    """Load config from <directory>/*.yml and optionally <directory>/env/*.yml 

    Files in the same directory may not overlap
    Config from <directory>/<env>/*.yml overwrites settings in <directory>/*.yml

    Args:
        directory (str): The base directory where the yaml-files lives (*.yml)
        env (str): An optional subdir of <directory> to get additional *.yml from

    Raises:
        HaipConfigException
    """
    global _config # pylint: disable=W0603
    config = _load_dir(directory)
    if env is not None:
        env_config = _load_dir(directory + os.sep + env)
        _merge(config, env_config, overwrite=True)
    _config = _make_container(config)
    return _config

def get(*paths, **options):
    """Get options from already loaded config.

    Args:
        *paths (non-keyworded args): Section names (str) leading to the section interested in.
        **options (keyworded args): options (option_name=option_default) you are intersted in. 
                                    Use keyword MANDATORY if the options must be set in the config.

    Raises:
        HaipConfigException

    Returns: 
        A dictionary (ConfigContainer) containing the whole section (if no options are given) or
        a dictionary (ConfigContainer) of the options requested. 

    Examples:

    config = { 
        'A' = {
            'B' = {
                'C' = {
                    'key1': 'value1',
                    'key2': 'value2'
                }
            }
        }
    }

    get('A', 'B') --> {'C' = {
                                'key1': 'value1',
                                'key2': 'value2'
                       }
    get('A', 'B', 'C', key1=MANDATORY) --> {'key1': 'value1'}
    get('A', 'B', 'C', key3=MANDATORY) --> ConfigHaipExcpetion (becaus key3 is mandatory but not found)
    get('A', 'B', 'C', key1=MANDATORY, key3='mydefault') --> {'key1': 'value1', 'key3': 'mydefault}
    
    PEP 468 preserves the order of **options (therefor python 3.6+ needed)
    """
    cfg = _goto(*paths)
    # return section if no options given
    if not options:
        return cfg
    # else provide options only
    result = ConfigContainer()
    for key, value in options.items():
        if key in cfg:
            result[key] = cfg[key]
        elif value is not MANDATORY:
            result[key] = value
        else:
            path = '/'.join(paths)
            raise HaipConfigException(f'option "{key}" not found in section "{path}"')
    return result

def set(*paths, **options):
    cfg = _goto(*paths)
    if not isinstance(cfg, dict):
        raise HaipConfigException(f'cannot set options in non-dict section')
    cfg.update(**options)

def _goto(*paths):
    fullpath = []
    cfg = _config
    for path in paths:
        fullpath.append(path)
        if path in cfg:
            cfg = cfg[path]
        else:
            fullpath = '.'.join(fullpath)
            raise HaipConfigException(f'path "{fullpath}" not found in config')
    return cfg

def _load_dir(directory):
    """ load all *.yml files from directory """
    _logger.info(f'load config from directory: {directory}')
    dir = pathlib.Path(directory)
    if not dir.exists():
        raise HaipConfigException(f'"{directory}" not found')        
    if not dir.is_dir():
        raise HaipConfigException(f'"{directory}" is not a directory')
    config = {}
    for file in dir.glob('*.yml'):
        _load_file(config, file)
    return config

def _load_file(config, file):
    """ load config from file and merge it into config """
    with open(file, 'r', encoding='utf-8') as ymlfile:
        ymlstring = ymlfile.read()
    file_config = poyo.parse_string(ymlstring)
    _merge(config, file_config, overwrite=False)

def _merge(d1, d2, overwrite=False):
    """ merge dict d2 into dict d1 """
    for k in d2:
        if k in d1:
            if isinstance(d1[k], dict) and isinstance(d2[k], dict):
                _merge(d1[k], d2[k], overwrite)
            elif overwrite:
                d1[k] = copy.deepcopy(d2[k])
            else:
                raise HaipConfigException(f'{k} defined multiple times')
        else:
            d1[k] = copy.deepcopy(d2[k])

def _make_container(config):
    if isinstance(config, dict):
        container = ConfigContainer()
        for k, v in config.items():
            if isinstance(v, dict):
                v = _make_container(v)
            container[k] = v
        return container
    return config

