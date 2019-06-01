from typing import Any, Callable
from unittest.mock import Mock

# from .models import MockExtensionGrammar, SideEffectBuilderGrammar
from .grammar import MockExtensionGrammar, SideEffectBuilderGrammar
from .side_effect import SideEffectBuilder

__all__ = (
    "allow",
    "return_value",
    "raise_exception",
    "receive_method",
    "be_called_with",
    "have_effect",
)


def allow(mock_subject: Mock) -> MockExtensionGrammar:
    """
    Prepare to extend a Mock from the Python Standard Library with a SideEffect.
    """
    return MockExtensionGrammar(mock_subject)


def return_value(return_value: Any) -> SideEffectBuilderGrammar:
    """
    Start building a side effect which returns a value when called.

    .. code:: python

        my_mock = Mock()
        allow(my_mock).to(return_value('fooby'))

        assert my_mock() == 'fooby'
    """
    builder = SideEffectBuilder().with_return_value(return_value)
    return SideEffectBuilderGrammar(builder=builder)


def return_(value: Any) -> SideEffectBuilderGrammar:
    """
    Alias for ``return_value``.
    """
    return return_value(value)


def raise_exception(raised_exception: Exception) -> SideEffectBuilderGrammar:
    """
    Start building a side effect which raises an exception.

    .. code:: python

        my_mock = Mock()
        allow(my_mock).to(raise_exception(ValueError))

        raised = False
        try:
            my_mock()
        except ValueError:
            raised = True
        assert raised
    """
    builder = SideEffectBuilder().with_raised_exception(raised_exception)
    return SideEffectBuilderGrammar(builder=builder)


def raise_(exception: Exception) -> SideEffectBuilderGrammar:
    """
    Alias for ``raise_exception``.
    """
    return raise_exception(exception)


def receive_method(name: str) -> SideEffectBuilderGrammar:
    """
    Start building a side effect on a named method of a Mock.

    .. code:: python

        my_mock = Mock()
        allow(my_mock).to(receive_method('foo').and_return('bar))

        assert my_mock.foo() == 'bar'
    """

    return SideEffectBuilderGrammar(method_name=name)


def receive(method_name: str) -> SideEffectBuilderGrammar:
    """
    Alias for ``receive_method``.
    """
    return receive_method(method_name)


def be_called_with(*args, **kwargs) -> SideEffectBuilderGrammar:
    """
    Start building a side effect which accepts arguments and keyword arguments

    .. code:: python

        my_mock = Mock()
        allow(my_mock).to(be_called_with('spam', foo='bar').and_return('eggs))

        assert my_mock('spam', foo='bar') == 'eggs'
    """
    builder = SideEffectBuilder().with_call_args(*args, **kwargs)
    return SideEffectBuilderGrammar(builder=builder)


def have_effect(effect: Callable) -> SideEffectBuilderGrammar:
    """
    Start building a side effect with a custom callable effect

    .. code:: python

        my_mock = Mock()
        def my_cool_effect(*args, **kwargs):
            print('hi')
            return args
        allow(my_mock).to(have_effect(my_cool_effect))

        assert my_mock(1, 2, 3) == [1, 2, 3]
        # >>> hi
    """
    builder = SideEffectBuilder().with_effect(effect)
    return SideEffectBuilderGrammar(builder=builder)
