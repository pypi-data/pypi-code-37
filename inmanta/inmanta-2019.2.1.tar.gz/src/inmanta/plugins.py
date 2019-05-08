"""
    Copyright 2017 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

import inspect
import subprocess
import os

from inmanta.execute.proxy import DynamicProxy
from inmanta.execute.util import Unknown
from inmanta.ast import Namespace, CompilerException, TypeNotFoundException, RuntimeException
from inmanta.execute.runtime import ExecutionUnit, Resolver, QueueScheduler, ResultVariable
from inmanta.ast.type import TypedList
from inmanta import protocol, const

from typing import Optional, Callable, List, TYPE_CHECKING, TypeVar, Any, Type

T = TypeVar("T")

if TYPE_CHECKING:
    from inmanta.ast.statements.call import FunctionCall
    from inmanta.ast.statements import ExpressionStatement, DynamicStatement
    from inmanta.compiler import Compiler


class Context(object):
    """
        An instance of this class is used to pass context to the plugin
    """
    __client: Optional[protocol.Client] = None
    __sync_client = None

    @classmethod
    def __get_client(cls) -> protocol.Client:
        if cls.__client is None:
            cls.__client = protocol.Client("compiler")
        return cls.__client

    def __init__(self, resolver: Resolver, queue: QueueScheduler, owner: "FunctionCall", result: ResultVariable) -> None:
        self.resolver = resolver
        self.queue = queue
        self.owner = owner
        self.result = result
        self.compiler = queue.get_compiler()

    def emit_expression(self, stmt: "ExpressionStatement") -> None:
        """
            Add a new statement
        """
        self.owner.copy_location(stmt)
        stmt.normalize(self.resolver)
        reqs = stmt.requires_emit(self.resolver, self.queue)
        ExecutionUnit(self.queue, self.resolver, self.result, reqs, stmt, provides=False)

    def get_resolver(self) -> Resolver:
        return self.resolver

    def get_type(self, name: str):
        """
            Get a type from the configuration model.
        """
        try:
            return self.queue.get_types()[name]
        except KeyError:
            raise TypeNotFoundException(name, self.owner.namespace)

    def get_queue_scheduler(self) -> QueueScheduler:
        return self.queue

    def get_compiler(self) -> "Compiler":
        return self.queue.get_compiler()

    def get_data_dir(self) -> str:
        """
            Get the path to the data dir (and create if it does not exist yet
        """
        data_dir = os.path.join("data", self.owner.function.namespace.get_full_name())

        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)

        return data_dir

    def get_client(self) -> protocol.Client:
        return self.__class__.__get_client()

    def get_sync_client(self) -> protocol.SyncClient:
        if self.__class__.__sync_client is None:
            self.__class__.__sync_client = protocol.SyncClient("compiler")
        return self.__class__.__sync_client

    def run_sync(self, function: Callable[..., T], timeout: int=5) -> T:
        """
            Execute the async function and return its result. This method takes care of starting and stopping the ioloop. The
            main use for this function is to use the inmanta internal rpc to communicate with the server.

            :param function: The async function to execute. This function should return a yieldable object.
            :param timeout: A timeout for the async function.
            :return: The result of the async call.
            :raises ConnectionRefusedError: When the function timeouts this exception is raised.
        """
        from tornado.ioloop import IOLoop, TimeoutError
        try:
            return IOLoop.current().run_sync(function, timeout)
        except TimeoutError:
            raise ConnectionRefusedError()


class PluginMeta(type):
    """
        A metaclass that registers subclasses in the parent class.
    """
    def __new__(cls, name, bases, dct):
        subclass = type.__new__(cls, name, bases, dct)
        if hasattr(subclass, "__function_name__"):
            cls.add_function(subclass)
        return subclass

    __functions = {}

    @classmethod
    def add_function(cls, plugin_class):
        """
            Add a function plugin class
        """
        name = plugin_class.__function_name__
        ns_parts = str(plugin_class.__module__).split(".")
        ns_parts.append(name)
        if ns_parts[0] != const.PLUGINS_PACKAGE:
            raise Exception(
                "All plugin modules should be loaded in the %s package" % const.PLUGINS_PACKAGE)

        name = "::".join(ns_parts[1:])
        cls.__functions[name] = plugin_class

    @classmethod
    def get_functions(cls):
        """
            Get all functions that are registered
        """
        return cls.__functions

    @classmethod
    def clear(cls) -> None:
        cls.__functions = {}


class Plugin(object, metaclass=PluginMeta):
    """
        This class models a plugin that can be called from the language.
    """

    def __init__(self, namespace: Namespace) -> None:
        self.ns = namespace

        self._context = -1
        self._return = None

        if hasattr(self.__class__, "__function__"):
            self.arguments = self._load_signature(self.__class__.__function__)
        else:
            self.arguments = []

        self.new_statement = None

    def normalize(self) -> None:
        self.resolver = self.namespace
        self.argtypes = [self.to_type(x[1], self.namespace) for x in self.arguments]
        self.returntype = self.to_type(self._return, self.namespace)

    def _load_signature(self, function):
        """
            Load the signature from the given python function
        """
        arg_spec = inspect.getfullargspec(function)
        if arg_spec.defaults is not None:
            default_start = len(arg_spec.args) - len(arg_spec.defaults)
        else:
            default_start = None

        arguments = []
        for i in range(len(arg_spec.args)):
            arg = arg_spec.args[i]

            if arg not in arg_spec.annotations:
                raise Exception("All arguments of plugin '%s' should be annotated" % function.__name__)

            spec_type = arg_spec.annotations[arg]
            if spec_type == Context:
                self._context = i
            else:
                if default_start is not None and default_start <= i:
                    default_value = arg_spec.defaults[default_start - i]

                    arguments.append((arg, spec_type, default_value))
                else:
                    arguments.append((arg, spec_type))

        if "return" in arg_spec.annotations:
            self._return = arg_spec.annotations["return"]

        return arguments

    def add_argument(self, arg_type, arg_type_name, arg_name, optional=False) -> None:
        """
            Add an argument at the next position, of given type.
        """
        self.arguments.append((arg_type, arg_type_name, arg_name, optional))

    def get_signature(self):
        """
            Generate the signature of this plugin
        """
        arg_list = []
        for arg in self.arguments:
            if len(arg) == 3:
                arg_list.append("%s: %s=%s" % (arg[0], arg[1], str(arg[2])))

            elif len(arg) == 2:
                arg_list.append("%s: %s" % (arg[0], arg[1]))

            else:
                arg_list.append(arg[0])

        args = ", ".join(arg_list)

        if self._return is None:
            return "%s(%s)" % (self.__class__.__function_name__, args)
        return "%s(%s) -> %s" % (self.__class__.__function_name__, args, self._return)

    def to_type(self, arg_type, resolver):
        """
            Convert a string representation of a type to a type
        """
        if arg_type is None:
            return None

        if not isinstance(arg_type, str):
            raise CompilerException("bad annotation in plugin %s::%s, expected str but got %s (%s)" %
                                    (self.ns, self.__class__.__function_name__, type(arg_type), arg_type))

        if arg_type == "any":
            return None

        if arg_type == "list":
            return list

        if arg_type == "expression":
            return None

        if arg_type.endswith("[]"):
            basetypename = arg_type[0:-2]
            basetype = resolver.get_type(basetypename)
            return TypedList(basetype)

        return resolver.get_type(arg_type)

    def _is_instance(self, value: Any, arg_type: Type) -> bool:
        """
            Check if value is of arg_type
        """
        if arg_type is None:
            return True

        if hasattr(arg_type, "validate"):
            return arg_type.validate(value)

        return isinstance(value, arg_type)

    def check_args(self, args: List[Any]) -> bool:
        """
            Check if the arguments of the call match the function signature
        """
        max_arg = len(self.arguments)
        required = len([x for x in self.arguments if len(x) == 2])

        if len(args) < required or len(args) > max_arg:
            raise Exception("Incorrect number of arguments for %s. Expected at least %d, got %d" %
                            (self.get_signature(), required, len(args)))

        for i in range(len(args)):
            if isinstance(args[i], Unknown):
                return False

            if self.arguments[i][0] is not None and not self._is_instance(args[i], self.argtypes[i]):
                raise Exception(("Invalid type for argument %d of '%s', it should be "
                                 "%s and %s given.") % (i + 1, self.__class__.__function_name__,
                                                        self.arguments[i][1], args[i].__class__.__name__))
        return True

    def emit_statement(self) -> "DynamicStatement":
        """
            This method is called to determine if the plugin call pushes a new
            statement
        """
        return self.new_statement

    def is_accept_unknowns(self):
        return self.opts["allow_unknown"]

    def get_variable(self, name, scope):
        """
            Get the given variable
        """
        return DynamicProxy.return_value(self._scope.get_variable(name, scope).value)

    def check_requirements(self) -> None:
        """
            Check if the plug-in has all it requires
        """
        if "bin" in self.opts and self.opts["bin"] is not None:
            for _bin in self.opts["bin"]:
                p = subprocess.Popen(["bash", "-c", "type -p %s" % _bin], stdout=subprocess.PIPE)
                result = p.communicate()

                if len(result[0]) == 0:
                    raise Exception("%s requires %s to be available in $PATH" % (self.__function_name__, _bin))

    def __call__(self, *args):
        """
            The function call itself
        """
        self.check_requirements()
        new_args = []
        for arg in args:
            if isinstance(arg, Context):
                new_args.append(arg)
            elif isinstance(arg, Unknown) and self.is_accept_unknowns():
                new_args.append(arg)
            else:
                new_args.append(DynamicProxy.return_value(arg))

        value = self.call(*new_args)

        value = DynamicProxy.unwrap(value)

        if self.returntype is not None and not isinstance(value, Unknown):
            valid = False
            exception = None

            try:
                valid = (value is None or self._is_instance(value, self.returntype))
            except RuntimeException as e:
                raise e
            except Exception as exp:
                exception = exp

            if not valid:
                msg = ""
                if exception is not None:
                    msg = "\n\tException details: " + str(exception)

                raise Exception("Plugin %s should return value of type %s ('%s' was returned) %s" %
                                (self.__class__.__function_name__, self.returntype, value, msg))

        return value


def plugin(function: Callable=None, commands: List[str]=None, emits_statements: bool=False,
           allow_unknown: bool=False) -> None:  # noqa: H801
    """
        Python decorator to register functions with inmanta as plugin

        :param function: The function to register with inmanta. This is the first argument when it is used as decorator.
        :param commands: A list of command paths that need to be available. Inmanta raises an exception when the command is
                         not available.
        :param emits_statements: Set to true if this plugin emits new statements that the compiler should execute. This is only
                                 required for complex plugins such as integrating a template engine.
        :param allow_unknown: Set to true if this plugin accepts Unknown values as valid input.
    """
    def curry_name(name=None, commands=None, emits_statements=False, allow_unknown=False):
        """
            Function to curry the name of the function
        """
        def call(fnc):
            """
                Create class to register the function and return the function itself
            """

            def wrapper(self, *args):
                """
                    Python will bind the function as method into the class
                """
                return fnc(*args)

            nonlocal name, commands, emits_statements

            if name is None:
                name = fnc.__name__

            dictionary = {}
            dictionary["__module__"] = fnc.__module__
            dictionary["__function_name__"] = name
            dictionary["opts"] = {"bin": commands, "emits_statements": emits_statements, "allow_unknown": allow_unknown}
            dictionary["call"] = wrapper
            dictionary["__function__"] = fnc

            bases = (Plugin,)
            PluginMeta.__new__(PluginMeta, name, bases, dictionary)

            return fnc

        return call

    if function is None:
        return curry_name(commands=commands, emits_statements=emits_statements, allow_unknown=allow_unknown)

    elif isinstance(function, str):
        return curry_name(function, commands=commands, emits_statements=emits_statements, allow_unknown=allow_unknown)

    elif function is not None:
        fnc = curry_name(commands=commands, emits_statements=emits_statements, allow_unknown=allow_unknown)
        return fnc(function)
