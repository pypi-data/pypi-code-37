import inspect
import logging
from enum import Enum

import google.protobuf.message
import google.protobuf.pyext._message
from google.protobuf.symbol_database import Default as get_grpc_symbol_database
from interface_meta import InterfaceMeta, override


GRPC_SYMBOL_DATABASE = get_grpc_symbol_database()


class GRPCMessageWrapperMeta(InterfaceMeta):

    _WRAPPERS = {}
    _ENUM_TYPES = {}

    def __register_implementation__(cls):
        if not cls._MESSAGE_TYPE:
            return

        if not inspect.isclass(cls._MESSAGE_TYPE) or not issubclass(cls._MESSAGE_TYPE, google.protobuf.message.Message):
            raise ValueError(f"Class `{cls.__name__}` has an invalid `_MESSAGE_TYPE`. Object of type `{cls._MESSAGE_TYPE.__class__.__name__}` is not a subclass of `google.protobuf.message.Message`.")

        # Register subclass
        cls._WRAPPERS[cls._MESSAGE_TYPE.DESCRIPTOR.full_name] = cls

        # Add message fields as attributes of the class
        for field, desc in cls._MESSAGE_TYPE.DESCRIPTOR.fields_by_name.items():

            if field in cls._IGNORED_FIELDS:
                continue

            if hasattr(cls, field):
                # Check that it is not a collision at the metaclass level
                collides_in_metaclass = True
                for base in cls.mro():
                    if field in base.__dict__:
                        collides_in_metaclass = False
                        break

                if not collides_in_metaclass:
                    logging.warning(f"Field `{field}` of `{cls._MESSAGE_TYPE}` is masked by class attributes.")
                    continue

            # Add field wrappers so that the attributes appear in class documentation
            setattr(
                cls, field, cls.__get_field_property_method(field)
            )

            # Add enum specifications to class definition
            if desc.enum_type:
                if desc.enum_type.full_name not in cls._ENUM_TYPES:
                    cls._ENUM_TYPES[desc.enum_type.full_name] = (
                        Enum(desc.enum_type.name, [
                            (v.name, v.number)
                            for v in desc.enum_type.values
                        ])
                    )

    def __get_field_property_method(cls, field):

        def get_field(self):
            return self.__getattr__(self, field)
        get_field.__name__ = field

        def set_field(self):
            return self.__setattr__(self, field)

        return property(fget=get_field, fset=set_field)

    def for_kind(cls, kind):
        if isinstance(kind, str):
            kind = GRPC_SYMBOL_DATABASE.GetSymbol(kind)
        assert inspect.isclass(kind) and issubclass(kind, google.protobuf.message.Message)
        if kind.DESCRIPTOR.full_name not in cls._WRAPPERS:
            GRPCMessageWrapperMeta(kind.DESCRIPTOR.full_name, (GRPCMessageWrapper, ), {'_MESSAGE_TYPE': kind})
        return cls._WRAPPERS[kind.DESCRIPTOR.full_name]

    def for_message(cls, message):
        if isinstance(message, google.protobuf.message.Message):
            return cls.for_kind(type(message))(message)
        return message

    def from_json(cls, json, message_type=None):
        message_type = message_type or getattr(cls, "_MESSAGE_TYPE", None)
        if not message_type:
            raise RuntimeError("`from_json()` can only be called on a wrapper which has `_MESSAGE_TYPE` set, or by passing in message_type specifically.")
        from google.protobuf.json_format import ParseDict
        return cls.for_message(ParseDict(json, message_type()))


class GRPCMessageWrapper(metaclass=GRPCMessageWrapperMeta):

    _MESSAGE_TYPE = None
    _IMMUTABLE_FIELDS = ()
    _IGNORED_FIELDS = ()

    __slots__ = ['__message', '__message_orig', '__persisted_fields']

    def __init__(self, _message=None, **kwargs):
        self.__persisted_fields = {}
        self.__message = _message or self._MESSAGE_TYPE()
        self._init(**kwargs)
        self.__message_orig = type(self.__message)()
        self.__message_orig.CopyFrom(self.__message)

    def _init(self, **kwargs):
        self << kwargs

    @property
    def _message(self):
        return self.__message

    def _update_from_pyobj(self, value):
        raise NotImplementedError

    def _as_pyobj(self):
        raise NotImplementedError

    def _rebase(self, message):
        self.__message = message or self._MESSAGE_TYPE()
        self.__message_orig.CopyFrom(message)

    def __dir__(self):
        return set([*(f.name for f in self.__message.DESCRIPTOR.fields if f.name not in self._IGNORED_FIELDS), *super().__dir__()])

    def __getattr__(self, attr, orig=False):
        descriptor = self._message.DESCRIPTOR.fields_by_name.get(attr)
        if not descriptor or attr in self._IGNORED_FIELDS:
            raise AttributeError(attr)

        if not orig and attr in self.__persisted_fields:
            return self.__persisted_fields[attr]

        if descriptor.label == descriptor.LABEL_REPEATED:
            value = GRPCRepeatedMessageWrapper(getattr(self.__message_orig if orig else self.__message, attr), wrapper=GRPCMessageWrapper.for_kind(descriptor.message_type.full_name) if descriptor.message_type else None)
        else:
            value = GRPCMessageWrapper.for_message(getattr(self.__message_orig if orig else self.__message, attr))

            if isinstance(value, GRPCMessageWrapper):
                try:
                    value = value._as_pyobj()
                except NotImplementedError:
                    pass
            elif descriptor.enum_type:
                value = GRPCMessageWrapper._ENUM_TYPES[descriptor.enum_type.full_name](value)

        if not orig:
            self.__persisted_fields[attr] = value

        return value

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            return super().__setattr__(attr, value)

        descriptor = self._message.DESCRIPTOR.fields_by_name.get(attr)
        if not descriptor or attr in self._IGNORED_FIELDS:
            raise AttributeError(attr)

        if attr in self._IMMUTABLE_FIELDS:
            raise AttributeError(f"{attr} is immutable.")

        if descriptor.enum_type:
            if self._MESSAGE_TYPE:
                enum_type = GRPCMessageWrapper._ENUM_TYPES[descriptor.enum_type.full_name]
                if isinstance(value, str):
                    value = enum_type[value]
                elif isinstance(value, int):
                    value = enum_type(value)
                if not isinstance(value, enum_type):
                    raise ValueError(value)
                value = value.value
            else:
                logging.warning(f"`{attr}` is an enum type, but messages of type `{self._message.__class__}` have not yet been individually wrapped and so only integer enum code will be accepted. Use with care.")

        self.__persisted_fields.pop(attr, None)

        wrapper = GRPCMessageWrapper.for_message(getattr(self.__message, attr))
        if isinstance(wrapper, GRPCMessageWrapper):
            return wrapper._update_from_pyobj(value)
        if value == descriptor.default_value:
            return self.__message.ClearField(attr)
        return self.__message.MergeFrom(self.__message.__class__(**{attr: value}))

    def __repr__(self):
        return f"GRPCMessageWrapper<{self.__class__.__name__}>"

    def __lshift__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        for key, value in other.items():
            setattr(self, key, value)
        return self

    @property
    def _changes(self):
        if self.__message == self.__message_orig:
            return print("No changes.")

        print(f"{self.__class__.__name__}:")
        for field in self.__message.DESCRIPTOR.fields:
            if getattr(self.__message, field.name) != getattr(self.__message_orig, field.name):
                print(f"{field.name}: {self.__getattr__(field.name, orig=True)} -> {getattr(self, field.name)}")

    def _to_json(self):
        from google.protobuf.json_format import MessageToDict
        return MessageToDict(self._message, including_default_value_fields=True)


class GRPCRepeatedMessageWrapper:

    def __init__(self, sequence, wrapper=None):
        self._sequence = sequence
        self._wrapper = wrapper

    def __wrapped(self, obj):
        return self._wrapper(obj) if self._wrapper else GRPCMessageWrapper.for_message(obj)

    def __iter__(self):
        for obj in self._sequence:
            yield self.__wrapped(obj)

    def __getitem__(self, index):
        return self.__wrapped(self._sequence[index])

    def __setitem__(self, index, value):
        pass

    def __delitem__(self, index):
        return self._sequence.__delitem__(index)

    def __repr__(self):
        return list(self).__repr__()

    def __len__(self):
        return len(self._sequence)

    def __add__(self, other):
        if isinstance(other, GRPCRepeatedMessageWrapper):
            self._sequence += other._sequence
        elif isinstance(other, (list, tuple)):
            self.extend(other)
        else:
            return NotImplemented
        return self

    def add(self, **kwargs):
        if isinstance(self._sequence, google.protobuf.pyext._message.RepeatedCompositeContainer):
            self.append(self._wrapper(**kwargs))
        else:
            RuntimeError("Addition is only supported for repeated composite containers. Use `.append()` for scalar values.")

    def append(self, obj):
        if isinstance(self._sequence, google.protobuf.pyext._message.RepeatedCompositeContainer):
            self._sequence.extend([obj._message if isinstance(obj, GRPCMessageWrapper) else obj])
        else:
            self._sequence.append(obj._message if isinstance(obj, GRPCMessageWrapper) else obj)

    def insert(self, index, obj):
        if isinstance(self._sequence, google.protobuf.pyext._message.RepeatedCompositeContainer):
            raise RuntimeError("Insertion is only supported for repeated scalar containers.")
        self._sequence.insert(index, obj._message if isinstance(obj, GRPCMessageWrapper) else obj)

    def extend(self, objs):
        for obj in objs:
            self.append(obj)

    def pop(self, index=-1):
        self._sequence.pop(index)


class GRPCInvisibleSequenceWrapper(GRPCMessageWrapper):

    _SEQUENCE_ATTR = None

    @override
    def _update_from_pyobj(self, value):
        sequence = getattr(self, self._SEQUENCE_ATTR)
        while sequence:
            sequence.pop()
        sequence.extend(v._message if isinstance(v, GRPCMessageWrapper) else v for v in value)

    @override
    def _as_pyobj(self):
        return getattr(self, self._SEQUENCE_ATTR)
