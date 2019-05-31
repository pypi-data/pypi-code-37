from __future__ import annotations

from typing import Callable, TypeVar, Union, Generic, Sequence, cast, Tuple, Dict, Any
import argparse
import builtins

T = TypeVar('T')


class InferTypeError(Exception):
    pass


class Value(Generic[T]):
    def __init__(
            self,
            default: T = None,
            *,
            type: type = None,
            choices: Sequence[T] = None,
            required: bool = False,
            nargs: Union[int, str] = None,
            help: str = None,
            metavar: Union[str, Tuple[str, ...]] = None,
    ) -> None:
        # infer type
        if type is None:
            if default is not None:
                if isinstance(default, (list, tuple)) and len(default) > 0:
                    type = builtins.type(default[0])
                else:
                    type = builtins.type(default)
            elif choices is not None and len(choices) > 0:
                type = builtins.type(choices[0])

        if type is None:
            raise InferTypeError('failed to infer type ({} {})'.format(default, choices))

        # check type
        if choices is not None:
            for v in choices:
                if not isinstance(v, type):
                    raise ValueError('type of value {} in choices is not {}'.format(default, type))

        # set nargs
        if nargs is None:
            if isinstance(default, (list, tuple)):
                nargs = '+'

        # check bool
        if type == bool and default != False:
            raise ValueError('bool type only supports store_true action.')

        self.type = type
        self.choices = choices
        self.required = required
        self.nargs = nargs
        self.help = help
        self.metavar = metavar
        self.set_default(default)

    def set_default(self, default):
        ''' update default value with type checking '''
        if default is not None:
            for v in default if isinstance(default, (list, tuple)) else [default]:
                if not isinstance(v, self.type):
                    raise ValueError('type of default value {} is not {}'.format(default, self.type))
        if self.required and default is not None:
            raise ValueError('required can be True only if default is None')
        self.default = default

    def add_argument(
            self,
            parser: argparse._ActionsContainer,
            name: str,
            dest: str = None,
    ) -> None:
        kwargs: Dict[str, Any] = {
            "default": self.default,
            "help": self.help,
        }
        if self.type == bool:
            kwargs["action"] = cast(argparse.Action, argparse._StoreTrueAction)
        else:
            kwargs["type"] = self.type
            kwargs["nargs"] = self.nargs
            kwargs["choices"] = self.choices
            kwargs["metavar"] = self.metavar
        if dest:
            kwargs["dest"] = dest
        if self.required:
            kwargs["required"] = self.required
        parser.add_argument(name, **kwargs)

    def __repr__(self) -> str:
        res = str(self.default) if not self.required else 'required'
        if self.choices is not None:
            res += ', one of [{}]'.format(', '.join(list(map(str, self.choices))))
        return '{}({})'.format(self.__class__.__name__, res)
