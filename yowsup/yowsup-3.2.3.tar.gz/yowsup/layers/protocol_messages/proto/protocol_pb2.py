# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protocol.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protocol.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x0eprotocol.proto\"R\n\nMessageKey\x12\x12\n\nremote_jid\x18\x01 \x01(\t\x12\x0f\n\x07\x66rom_me\x18\x02 \x01(\x08\x12\n\n\x02id\x18\x03 \x01(\t\x12\x13\n\x0bparticipant\x18\x04 \x01(\t')
)




_MESSAGEKEY = _descriptor.Descriptor(
  name='MessageKey',
  full_name='MessageKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='remote_jid', full_name='MessageKey.remote_jid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_me', full_name='MessageKey.from_me', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='MessageKey.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='participant', full_name='MessageKey.participant', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=100,
)

DESCRIPTOR.message_types_by_name['MessageKey'] = _MESSAGEKEY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MessageKey = _reflection.GeneratedProtocolMessageType('MessageKey', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGEKEY,
  __module__ = 'protocol_pb2'
  # @@protoc_insertion_point(class_scope:MessageKey)
  ))
_sym_db.RegisterMessage(MessageKey)


# @@protoc_insertion_point(module_scope)
