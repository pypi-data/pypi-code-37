from itertools import chain, repeat
from unittest.mock import call
from typing import Any, Callable

from .exception import AllowsException


class SideEffectBuilder:
    """
    Uses builder pattern to set up Callable effect and Call argument values for
    SideEffect objects.

    Only one effect can be applied in a given builder (return, exception, effect).
    """

    def __init__(self, call_args=None, effect=None) -> None:
        self._call_args = call_args
        self._effect = effect

    def with_call_args(self, *args, **kwargs):
        """ Only invoke side effect when certain args are present """
        if self._call_args:
            raise AllowsException("Cannot set multiple call args in one effect")
        self._call_args = call(*args, **kwargs)
        return self

    def with_raised_exception(self, raised_exception: Exception):
        """ Raise an exception. """

        def raise_(*args, **kwargs):
            raise raised_exception

        effect = raise_
        return self._set_effect(effect)

    def with_return_value(self, *return_values: Any):
        """ Add a return value. """
        return_value_iterator = iter(chain(return_values, repeat(return_values[-1])))

        def return_next(*args, **kwargs):
            return next(return_value_iterator)

        effect = return_next
        return self._set_effect(effect)

    def with_effect(self, effect: Callable):
        """ Add a generic effect to the side effect. """
        return self._set_effect(effect)

    def _set_effect(self, effect: Callable):
        if self._effect:
            raise AllowsException("Cannot set multiple effects")

        self._effect = lambda *args, **kwargs: effect(*args, **kwargs)
        return self

    def build(self):
        """ Create the side effect. """
        return SideEffect(call_args=self._call_args, effect=self._effect)


def no_op(*args, **kwargs):
    return


class SideEffect:
    """
    Callable object that can compose many side effects with corresponding arguments or
    default response.
    """

    def __init__(self, call_args=None, effect=None, default_effect=None):
        if not call_args and effect:
            default_effect = effect
            effect = None
        elif not call_args and not effect:
            call_args = call()
            effect = no_op
        self._calls = [call_args] if call_args else []
        self._effects = [effect] if effect and call_args else []
        self._default_effect = default_effect

    def __call__(self, *args, **kwargs):
        call_args = call(*args, **kwargs)
        effect = self._effect_lookup(call_args)
        return effect(*args, **kwargs)

    def _effect_lookup(self, call_args):
        effect = None
        try:
            call_index = self._calls.index(call_args)
            effect = self._effects[call_index]
        except ValueError:
            effect = self._default_effect
        return effect

    def merge(self, other: "SideEffect") -> "SideEffect":
        """ Build a new SideEffect from this one and another """
        if other is None:
            return self
        if isinstance(other, self.__class__):
            self._calls.extend(other._calls)
            self._effects.extend(other._effects)
            self._default_effect = self._default_effect or other._default_effect
            return self
        raise AllowsException("Cannot merge effects that are not SideEffect")
