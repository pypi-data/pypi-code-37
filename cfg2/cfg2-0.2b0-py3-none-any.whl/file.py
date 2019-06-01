from ._logging import logger
from .errors import *
log = logger.getChild('file')
from .data import DictProxy

def _yaml_load(stream):
    import yaml
    return yaml.load(stream,Loader=yaml.SafeLoader)

def _json_load(stream):
    import json
    return json.load(stream)

loaders = {
  'yml': _yaml_load,
  'yaml': _yaml_load,
  'js': _json_load,
  'json': _json_load
}

def _file_load(filename):
    import pathlib2
    path = pathlib2.Path(filename).absolute()
    ext = path.name.split('.')[-1]
    loader = loaders[ext]
    with path.open('r') as stream:
        data = loader(stream)
    return data

def dictproxy_load(self,filename=None):
    if filename is None:
        filename = self.__filename__
    else:
        self.__filename__ = filename
    data = _file_load(filename)
    if not isinstance(data,self.__datatype__):
        raise TypeError(type(data).__name__)
    self.__datatype__.clear(self)
    self.__content__ = data
DictProxy.load = dictproxy_load

def ConfigFile(filename):
    cfg = DictProxy()
    cfg.load(filename)
    return cfg

def _yaml_dump(data,stream):
    import yaml
    return yaml.dump(data,stream,Dumper=yaml.SafeDumper)

def _json_dump(data,stream):
    import json
    return json.dump(data,stream)

dumpers = {
    'yml': _yaml_dump,
    'yaml': _yaml_dump,
    'js': _json_dump,
    'json': _json_dump,
}

def _file_dump(data,filename):
    import pathlib2
    path = pathlib2.Path(filename).absolute()
    ext = path.name.split('.')[-1]
    dumper = dumpers[ext]
    with path.open('w') as stream:
        dumper(data,stream)

def dictproxy_dump(self,filename=None):
    if filename is None:
        filename = self.__filename__
    else:
        self.__filename__ = filename
    _file_dump(self.__content__,filename)
DictProxy.dump = dictproxy_dump

__all__ = ['ConfigFile']
