# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import variant_pb2 as variant__pb2
from . import agent_info_pb2 as agent__info__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='com.rookout',
  syntax='proto3',
  serialized_pb=_b('\n\x0emessages.proto\x12\x0b\x63om.rookout\x1a\rvariant.proto\x1a\x10\x61gent_info.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"D\n\x0fNewAgentMessage\x12\x31\n\nagent_info\x18\x01 \x01(\x0b\x32\x1d.com.rookout.AgentInformation\">\n\nStackFrame\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04line\x18\x02 \x01(\r\x12\x10\n\x08\x66unction\x18\x03 \x01(\t\"5\n\nStackTrace\x12\'\n\x06\x66rames\x18\x01 \x03(\x0b\x32\x17.com.rookout.StackFrame\"~\n\tException\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12&\n\x08instance\x18\x03 \x01(\x0b\x32\x14.com.rookout.Variant\x12*\n\ttraceback\x18\x04 \x01(\x0b\x32\x17.com.rookout.StackTrace\"\xcb\x03\n\nLogMessage\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08\x61gent_id\x18\x02 \x01(\t\x12/\n\x05level\x18\x03 \x01(\x0e\x32 .com.rookout.LogMessage.LogLevel\x12\x10\n\x08\x66ilename\x18\x04 \x01(\t\x12\x0c\n\x04line\x18\x05 \x01(\r\x12\x0c\n\x04text\x18\x06 \x01(\t\x12\'\n\targuments\x18\x07 \x03(\x0b\x32\x14.com.rookout.Variant\x12)\n\texception\x18\x08 \x01(\x0b\x32\x16.com.rookout.Exception\x12\x1d\n\x11\x66ormatted_message\x18\t \x01(\tB\x02\x18\x01\x12\x32\n\x10legacy_arguments\x18\n \x01(\x0b\x32\x14.com.rookout.VariantB\x02\x18\x01\x12\x12\n\nclass_name\x18\x0b \x01(\t\x12\x13\n\x0bmethod_name\x18\x0c \x01(\t\"M\n\x08LogLevel\x12\t\n\x05TRACE\x10\x00\x12\t\n\x05\x44\x45\x42UG\x10\x01\x12\x08\n\x04INFO\x10\x02\x12\x0b\n\x07WARNING\x10\x03\x12\t\n\x05\x45RROR\x10\x04\x12\t\n\x05\x46\x41TAL\x10\x05\"i\n\x11RuleStatusMessage\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\t\x12\x0f\n\x07rule_id\x18\x02 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x03 \x01(\t\x12!\n\x05\x65rror\x18\x04 \x01(\x0b\x32\x12.com.rookout.Error\"]\n\x10\x41ugReportMessage\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\t\x12\x0e\n\x06\x61ug_id\x18\x02 \x01(\t\x12\'\n\targuments\x18\x03 \x01(\x0b\x32\x14.com.rookout.Variant\"!\n\rAddAugCommand\x12\x10\n\x08\x61ug_json\x18\x01 \x01(\t\"\"\n\x12InitialAugsCommand\x12\x0c\n\x04\x61ugs\x18\x01 \x03(\t\"\"\n\x10RemoveAugCommand\x12\x0e\n\x06\x61ug_id\x18\x01 \x01(\t\"\x15\n\x13InitFinishedMessage\"\x12\n\x10\x43learAugsCommand\"\x1c\n\x0bPingMessage\x12\r\n\x05value\x18\x01 \x01(\x05\"\x1f\n\x0c\x45rrorMessage\x12\x0f\n\x07message\x18\x01 \x01(\tb\x06proto3')
  ,
  dependencies=[variant__pb2.DESCRIPTOR,agent__info__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])



_LOGMESSAGE_LOGLEVEL = _descriptor.EnumDescriptor(
  name='LogLevel',
  full_name='com.rookout.LogMessage.LogLevel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TRACE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEBUG', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INFO', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WARNING', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FATAL', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=797,
  serialized_end=874,
)
_sym_db.RegisterEnumDescriptor(_LOGMESSAGE_LOGLEVEL)


_NEWAGENTMESSAGE = _descriptor.Descriptor(
  name='NewAgentMessage',
  full_name='com.rookout.NewAgentMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agent_info', full_name='com.rookout.NewAgentMessage.agent_info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=97,
  serialized_end=165,
)


_STACKFRAME = _descriptor.Descriptor(
  name='StackFrame',
  full_name='com.rookout.StackFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='com.rookout.StackFrame.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='line', full_name='com.rookout.StackFrame.line', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='function', full_name='com.rookout.StackFrame.function', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=167,
  serialized_end=229,
)


_STACKTRACE = _descriptor.Descriptor(
  name='StackTrace',
  full_name='com.rookout.StackTrace',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frames', full_name='com.rookout.StackTrace.frames', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=231,
  serialized_end=284,
)


_EXCEPTION = _descriptor.Descriptor(
  name='Exception',
  full_name='com.rookout.Exception',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='com.rookout.Exception.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='com.rookout.Exception.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='instance', full_name='com.rookout.Exception.instance', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='traceback', full_name='com.rookout.Exception.traceback', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=286,
  serialized_end=412,
)


_LOGMESSAGE = _descriptor.Descriptor(
  name='LogMessage',
  full_name='com.rookout.LogMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='com.rookout.LogMessage.timestamp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='agent_id', full_name='com.rookout.LogMessage.agent_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='level', full_name='com.rookout.LogMessage.level', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='filename', full_name='com.rookout.LogMessage.filename', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='line', full_name='com.rookout.LogMessage.line', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='text', full_name='com.rookout.LogMessage.text', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='com.rookout.LogMessage.arguments', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exception', full_name='com.rookout.LogMessage.exception', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='formatted_message', full_name='com.rookout.LogMessage.formatted_message', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\030\001'))),
    _descriptor.FieldDescriptor(
      name='legacy_arguments', full_name='com.rookout.LogMessage.legacy_arguments', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\030\001'))),
    _descriptor.FieldDescriptor(
      name='class_name', full_name='com.rookout.LogMessage.class_name', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='method_name', full_name='com.rookout.LogMessage.method_name', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LOGMESSAGE_LOGLEVEL,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=415,
  serialized_end=874,
)


_RULESTATUSMESSAGE = _descriptor.Descriptor(
  name='RuleStatusMessage',
  full_name='com.rookout.RuleStatusMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agent_id', full_name='com.rookout.RuleStatusMessage.agent_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rule_id', full_name='com.rookout.RuleStatusMessage.rule_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='active', full_name='com.rookout.RuleStatusMessage.active', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error', full_name='com.rookout.RuleStatusMessage.error', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=876,
  serialized_end=981,
)


_AUGREPORTMESSAGE = _descriptor.Descriptor(
  name='AugReportMessage',
  full_name='com.rookout.AugReportMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agent_id', full_name='com.rookout.AugReportMessage.agent_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aug_id', full_name='com.rookout.AugReportMessage.aug_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='com.rookout.AugReportMessage.arguments', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=983,
  serialized_end=1076,
)


_ADDAUGCOMMAND = _descriptor.Descriptor(
  name='AddAugCommand',
  full_name='com.rookout.AddAugCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='aug_json', full_name='com.rookout.AddAugCommand.aug_json', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1078,
  serialized_end=1111,
)


_INITIALAUGSCOMMAND = _descriptor.Descriptor(
  name='InitialAugsCommand',
  full_name='com.rookout.InitialAugsCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='augs', full_name='com.rookout.InitialAugsCommand.augs', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1113,
  serialized_end=1147,
)


_REMOVEAUGCOMMAND = _descriptor.Descriptor(
  name='RemoveAugCommand',
  full_name='com.rookout.RemoveAugCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='aug_id', full_name='com.rookout.RemoveAugCommand.aug_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1149,
  serialized_end=1183,
)


_INITFINISHEDMESSAGE = _descriptor.Descriptor(
  name='InitFinishedMessage',
  full_name='com.rookout.InitFinishedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1185,
  serialized_end=1206,
)


_CLEARAUGSCOMMAND = _descriptor.Descriptor(
  name='ClearAugsCommand',
  full_name='com.rookout.ClearAugsCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1208,
  serialized_end=1226,
)


_PINGMESSAGE = _descriptor.Descriptor(
  name='PingMessage',
  full_name='com.rookout.PingMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='com.rookout.PingMessage.value', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1228,
  serialized_end=1256,
)


_ERRORMESSAGE = _descriptor.Descriptor(
  name='ErrorMessage',
  full_name='com.rookout.ErrorMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='com.rookout.ErrorMessage.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1258,
  serialized_end=1289,
)

_NEWAGENTMESSAGE.fields_by_name['agent_info'].message_type = agent__info__pb2._AGENTINFORMATION
_STACKTRACE.fields_by_name['frames'].message_type = _STACKFRAME
_EXCEPTION.fields_by_name['instance'].message_type = variant__pb2._VARIANT
_EXCEPTION.fields_by_name['traceback'].message_type = _STACKTRACE
_LOGMESSAGE.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LOGMESSAGE.fields_by_name['level'].enum_type = _LOGMESSAGE_LOGLEVEL
_LOGMESSAGE.fields_by_name['arguments'].message_type = variant__pb2._VARIANT
_LOGMESSAGE.fields_by_name['exception'].message_type = _EXCEPTION
_LOGMESSAGE.fields_by_name['legacy_arguments'].message_type = variant__pb2._VARIANT
_LOGMESSAGE_LOGLEVEL.containing_type = _LOGMESSAGE
_RULESTATUSMESSAGE.fields_by_name['error'].message_type = variant__pb2._ERROR
_AUGREPORTMESSAGE.fields_by_name['arguments'].message_type = variant__pb2._VARIANT
DESCRIPTOR.message_types_by_name['NewAgentMessage'] = _NEWAGENTMESSAGE
DESCRIPTOR.message_types_by_name['StackFrame'] = _STACKFRAME
DESCRIPTOR.message_types_by_name['StackTrace'] = _STACKTRACE
DESCRIPTOR.message_types_by_name['Exception'] = _EXCEPTION
DESCRIPTOR.message_types_by_name['LogMessage'] = _LOGMESSAGE
DESCRIPTOR.message_types_by_name['RuleStatusMessage'] = _RULESTATUSMESSAGE
DESCRIPTOR.message_types_by_name['AugReportMessage'] = _AUGREPORTMESSAGE
DESCRIPTOR.message_types_by_name['AddAugCommand'] = _ADDAUGCOMMAND
DESCRIPTOR.message_types_by_name['InitialAugsCommand'] = _INITIALAUGSCOMMAND
DESCRIPTOR.message_types_by_name['RemoveAugCommand'] = _REMOVEAUGCOMMAND
DESCRIPTOR.message_types_by_name['InitFinishedMessage'] = _INITFINISHEDMESSAGE
DESCRIPTOR.message_types_by_name['ClearAugsCommand'] = _CLEARAUGSCOMMAND
DESCRIPTOR.message_types_by_name['PingMessage'] = _PINGMESSAGE
DESCRIPTOR.message_types_by_name['ErrorMessage'] = _ERRORMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NewAgentMessage = _reflection.GeneratedProtocolMessageType('NewAgentMessage', (_message.Message,), dict(
  DESCRIPTOR = _NEWAGENTMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.NewAgentMessage)
  ))
_sym_db.RegisterMessage(NewAgentMessage)

StackFrame = _reflection.GeneratedProtocolMessageType('StackFrame', (_message.Message,), dict(
  DESCRIPTOR = _STACKFRAME,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.StackFrame)
  ))
_sym_db.RegisterMessage(StackFrame)

StackTrace = _reflection.GeneratedProtocolMessageType('StackTrace', (_message.Message,), dict(
  DESCRIPTOR = _STACKTRACE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.StackTrace)
  ))
_sym_db.RegisterMessage(StackTrace)

Exception = _reflection.GeneratedProtocolMessageType('Exception', (_message.Message,), dict(
  DESCRIPTOR = _EXCEPTION,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.Exception)
  ))
_sym_db.RegisterMessage(Exception)

LogMessage = _reflection.GeneratedProtocolMessageType('LogMessage', (_message.Message,), dict(
  DESCRIPTOR = _LOGMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.LogMessage)
  ))
_sym_db.RegisterMessage(LogMessage)

RuleStatusMessage = _reflection.GeneratedProtocolMessageType('RuleStatusMessage', (_message.Message,), dict(
  DESCRIPTOR = _RULESTATUSMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.RuleStatusMessage)
  ))
_sym_db.RegisterMessage(RuleStatusMessage)

AugReportMessage = _reflection.GeneratedProtocolMessageType('AugReportMessage', (_message.Message,), dict(
  DESCRIPTOR = _AUGREPORTMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.AugReportMessage)
  ))
_sym_db.RegisterMessage(AugReportMessage)

AddAugCommand = _reflection.GeneratedProtocolMessageType('AddAugCommand', (_message.Message,), dict(
  DESCRIPTOR = _ADDAUGCOMMAND,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.AddAugCommand)
  ))
_sym_db.RegisterMessage(AddAugCommand)

InitialAugsCommand = _reflection.GeneratedProtocolMessageType('InitialAugsCommand', (_message.Message,), dict(
  DESCRIPTOR = _INITIALAUGSCOMMAND,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.InitialAugsCommand)
  ))
_sym_db.RegisterMessage(InitialAugsCommand)

RemoveAugCommand = _reflection.GeneratedProtocolMessageType('RemoveAugCommand', (_message.Message,), dict(
  DESCRIPTOR = _REMOVEAUGCOMMAND,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.RemoveAugCommand)
  ))
_sym_db.RegisterMessage(RemoveAugCommand)

InitFinishedMessage = _reflection.GeneratedProtocolMessageType('InitFinishedMessage', (_message.Message,), dict(
  DESCRIPTOR = _INITFINISHEDMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.InitFinishedMessage)
  ))
_sym_db.RegisterMessage(InitFinishedMessage)

ClearAugsCommand = _reflection.GeneratedProtocolMessageType('ClearAugsCommand', (_message.Message,), dict(
  DESCRIPTOR = _CLEARAUGSCOMMAND,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.ClearAugsCommand)
  ))
_sym_db.RegisterMessage(ClearAugsCommand)

PingMessage = _reflection.GeneratedProtocolMessageType('PingMessage', (_message.Message,), dict(
  DESCRIPTOR = _PINGMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.PingMessage)
  ))
_sym_db.RegisterMessage(PingMessage)

ErrorMessage = _reflection.GeneratedProtocolMessageType('ErrorMessage', (_message.Message,), dict(
  DESCRIPTOR = _ERRORMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.ErrorMessage)
  ))
_sym_db.RegisterMessage(ErrorMessage)


_LOGMESSAGE.fields_by_name['formatted_message'].has_options = True
_LOGMESSAGE.fields_by_name['formatted_message']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\030\001'))
_LOGMESSAGE.fields_by_name['legacy_arguments'].has_options = True
_LOGMESSAGE.fields_by_name['legacy_arguments']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\030\001'))
# @@protoc_insertion_point(module_scope)
