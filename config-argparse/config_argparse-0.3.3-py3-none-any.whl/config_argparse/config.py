from __future__ import annotations

from typing import Callable, List, Set, Tuple, Type, Any, MutableMapping, Mapping, cast, Union, Sequence, TypeVar, Generic, Optional
from collections import abc
import argparse
import copy
import inspect
from .argparse_action import NoOpAction
from .value import Value

T = TypeVar('T', bound=MutableMapping[Any, Any])
C = TypeVar('C', bound='Config')


class Config(MutableMapping[str, Any]):
    def __init__(self: C, default: Mapping[str, Any] = None):
        self._children: MutableMapping[str, Union[Config, DynamicConfig, Value]] = {}
        self._default: MutableMapping[str, Any] = {}
        for name, value in _collect_class_variables(self.__class__).items():  # generates copy of class variables
            if not isinstance(value, (Config, DynamicConfig, Value)):
                value = Value(value)
            self._children[name] = value

        self.set_default(default if default is not None else {})

    def _reload(self: C):
        # reload Config & Value first
        # because they will be used to determine the contents of DynamicConfig
        for name, value in self._children.items():
            if isinstance(value, Config):
                setattr(self, name, type(value)(value._default))
            elif isinstance(value, Value):
                setattr(self, name, copy.deepcopy(value.default))
        # reload DynamicConfig
        for name, value in self._children.items():
            if isinstance(value, DynamicConfig):
                setattr(self, name, value(self))

    def set_default(self: C, values: Mapping[str, Any]):
        self._default.update(values)
        for name, value in values.items():
            self._children[name].set_default(value)
        self._reload()

    def parse_known_args(
            self: C,
            args: List[str] = None,
            prefix='',
            namespace: T = None,
    ) -> Tuple[Union[C, T], List[str]]:
        if args is None:
            args = []
        if namespace is None:
            namespace2: Union[C, T] = type(self)(self._default)
        else:
            namespace2 = namespace

        def is_name(s):
            return s.startswith('--')

        left_args: Set[str] = set(filter(is_name, args))
        # parse Values
        parser = argparse.ArgumentParser(self.__class__.__name__, allow_abbrev=False)
        self._add_arguments(parser, prefix)
        if '--' + prefix + 'help' in args:
            parser.print_help()
            parser.exit()
        _, left = parser.parse_known_args(args, namespace=namespace2)  # type: ignore
        left_args = left_args & set(filter(is_name, left))
        # parse Config & DynamicConfig
        left_args = left_args & self._parse_config(args, prefix, namespace2)

        return namespace2, list(left_args)

    def parse_args(self: C, *args, **kwargs) -> C:
        namespace, left_args = self.parse_known_args(*args, **kwargs)
        if len(left_args) > 0:
            raise Exception('unknown arguments: {}'.format(left_args))
        return namespace

    def todict(self: C) -> Mapping[str, Any]:
        res = {}
        for name in self._children.keys():
            res[name] = getattr(self, name)
            if isinstance(res[name], Config):
                res[name] = res[name].todict()
            if isinstance(res[name], (list, tuple)):
                for i, v in enumerate(res[name]):
                    if isinstance(v, Config):
                        res[name][i] = v.todict()
        return res

    def _add_arguments(
            self,
            parser: argparse._ActionsContainer,
            prefix: str,
    ):
        for class_variable, value in self._children.items():
            name = '--' + prefix + class_variable
            if isinstance(value, (Config, DynamicConfig)):
                parser.add_argument(name, action=NoOpAction, dest=class_variable)
            elif isinstance(value, Value):
                value.add_argument(parser, name, dest=class_variable)
            else:
                assert False

    def _parse_config(
            self,
            args: List[str],
            prefix: str,
            namespace: T,
    ) -> Set[str]:
        left = set(filter(lambda s: s.startswith('--'), args))
        # we assume Values are already parsed
        # parse Config
        for class_variable, val in self._children.items():
            if isinstance(val, Config):
                dest = prefix + class_variable
                name = '--' + dest

                sub_namespace, l = val.parse_known_args(
                    args,
                    prefix=dest + '.',
                    namespace=cast(Optional[T], namespace.get(class_variable, None)),
                )
                namespace[class_variable] = sub_namespace
                left = left & set(l)
        # parse DynamicConfig
        for class_variable, val in self._children.items():
            if isinstance(val, DynamicConfig):
                dest = prefix + class_variable
                name = '--' + dest

                sub_namespace2, l, _ = val.parse_args(
                    namespace,
                    args,
                    prefix=dest + '.',
                    namespace=cast(Union[T, List[T], None], namespace.get(class_variable, None)),
                )
                namespace[class_variable] = sub_namespace2
                left = left & set(l)
        return left

    def __repr__(self):
        res = ['{}:'.format(self.__class__.__name__)]
        for class_variable in self:
            txt = str(self[class_variable]).replace('\n', '\n\t')
            res.append('\t{} = {}'.format(class_variable, txt))
        return '\n'.join(res)

    def __getitem__(self, key):
        if key not in self._children:
            raise KeyError
        return getattr(self, key)

    def __setitem__(self, key, value):
        # note: this value is not transferred to returned value of parse_args()
        if key not in self._children:
            raise KeyError
        setattr(self, key, value)

    def __delitem__(self, key):
        # note: this operation is not transferred to returned value of parse_args()
        delattr(self, key)

    def __iter__(self):
        for key in self._children.keys():
            yield key

    def __len__(self):
        return len(self._children)


class DynamicConfig():
    def __init__(self, config_factory: Callable[[T], Union[Config, Sequence[Config]]], auto_load=False):
        self.config_factory = config_factory
        self._defaults: List[Union[Mapping[str, Any], List[Mapping[str, Any]]]] = []
        self.auto_load = auto_load

    def set_default(self, values: Union[Mapping[str, Any], List[Mapping[str, Any]]]):
        self._defaults.append(values)

    def parse_args(
            self,
            parent_config: T,
            args: List[str],
            prefix: str,
            namespace: Union[T, List[T], None] = None,
    ) -> Tuple[Union[T, List[T], None], List[str], Union[Config, Sequence[Config], None]]:
        configs = self._load(parent_config)
        if configs is None:
            assert namespace is None
            return None, args, None
        elif isinstance(configs, Config):
            assert not isinstance(namespace, list)
            ns, left_args = configs.parse_known_args(args, prefix, namespace=namespace)
            return cast(T, ns), left_args, configs
        else:
            if namespace is None:
                ns_list: List[Optional[T]] = [None for _ in configs]
            else:
                assert isinstance(namespace, list)
                ns_list = cast(List[Optional[T]], namespace)

            left_args2 = set(args)
            for i, config in enumerate(configs):
                ns, a_left_args = config.parse_known_args(args, prefix, namespace=ns_list[i])
                ns_list[i] = cast(T, ns)
                left_args2 &= set(a_left_args)
            ns_list2 = cast(List[T], ns_list)
            return ns_list2, list(left_args2), configs

    def __call__(self, parent_config: T):
        if not self.auto_load:
            return None
        return self._load(parent_config)

    def _load(self, parent_config: T) -> Union[Config, Sequence[Config], None]:
        configs = self.config_factory(parent_config)
        defaults = self._defaults

        if configs is None:
            if len(defaults) > 0:
                raise Exception('DynamicConfig: config_factory returned None, but default values exist {}'.format(defaults))
            return None

        if isinstance(configs, Config):
            for default in defaults:
                assert not isinstance(default, list)
                configs.set_default(default)
            return configs

        for config in configs:
            if not isinstance(config, Config):
                raise Exception('DynamicConfig: config_factory should return instance of Config or [Config], but returned {}'.format(config))
        for default in defaults:
            assert isinstance(
                default,
                list) and len(default) == len(configs), 'DynamicConfig: config_factory returned {} Configs, but length of default {} is {}.'.format(
                    len(configs), default, len(default))

            for config, a_default in zip(configs, default):
                config.set_default(a_default)
        return configs


def _collect_class_variables(cls):
    ''' return copy of all class variables which name do not start with underscore '''
    res = {}
    for base in filter(lambda b: issubclass(b, Config), reversed(cls.__bases__)):
        res.update(_collect_class_variables(base))
    for member in cls.__dict__.keys():
        if not member.startswith('_') and not inspect.isfunction(cls.__dict__[member]):
            res[member] = copy.deepcopy(cls.__dict__[member])
    return res
