# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: indoor_temperature_prediction.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='indoor_temperature_prediction.proto',
  package='thermal_model',
  syntax='proto3',
  serialized_options=_b('P\001'),
  serialized_pb=_b('\n#indoor_temperature_prediction.proto\x12\rthermal_model\"\x83\x03\n\x1cSecondOrderPredictionRequest\x12\x10\n\x08\x62uilding\x18\x01 \x01(\t\x12\x0c\n\x04zone\x18\x02 \x01(\t\x12\x14\n\x0c\x63urrent_time\x18\x03 \x01(\x03\x12\x0e\n\x06\x61\x63tion\x18\x04 \x01(\x03\x12\x1a\n\x12indoor_temperature\x18\x05 \x01(\x01\x12#\n\x1bprevious_indoor_temperature\x18\x06 \x01(\x01\x12\x1b\n\x13outside_temperature\x18\x07 \x01(\x01\x12g\n\x17other_zone_temperatures\x18\x08 \x03(\x0b\x32\x46.thermal_model.SecondOrderPredictionRequest.OtherZoneTemperaturesEntry\x12\x18\n\x10temperature_unit\x18\t \x01(\t\x1a<\n\x1aOtherZoneTemperaturesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\"h\n\x0c\x45rrorRequest\x12\x10\n\x08\x62uilding\x18\x01 \x01(\t\x12\x0c\n\x04zone\x18\x02 \x01(\t\x12\x0e\n\x06\x61\x63tion\x18\x03 \x01(\x03\x12\r\n\x05start\x18\x04 \x01(\x03\x12\x0b\n\x03\x65nd\x18\x05 \x01(\x03\x12\x0c\n\x04unit\x18\x06 \x01(\t\"L\n\x19PredictedTemperatureReply\x12\x0c\n\x04time\x18\x01 \x01(\x03\x12\x13\n\x0btemperature\x18\x02 \x01(\x01\x12\x0c\n\x04unit\x18\x03 \x01(\t\"5\n\nErrorReply\x12\x0c\n\x04mean\x18\x01 \x01(\x01\x12\x0b\n\x03var\x18\x02 \x01(\x01\x12\x0c\n\x04unit\x18\x03 \x01(\t2\xe3\x01\n\x1bIndoorTemperaturePrediction\x12s\n\x18GetSecondOrderPrediction\x12+.thermal_model.SecondOrderPredictionRequest\x1a(.thermal_model.PredictedTemperatureReply\"\x00\x12O\n\x13GetSecondOrderError\x12\x1b.thermal_model.ErrorRequest\x1a\x19.thermal_model.ErrorReply\"\x00\x42\x02P\x01\x62\x06proto3')
)




_SECONDORDERPREDICTIONREQUEST_OTHERZONETEMPERATURESENTRY = _descriptor.Descriptor(
  name='OtherZoneTemperaturesEntry',
  full_name='thermal_model.SecondOrderPredictionRequest.OtherZoneTemperaturesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='thermal_model.SecondOrderPredictionRequest.OtherZoneTemperaturesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='thermal_model.SecondOrderPredictionRequest.OtherZoneTemperaturesEntry.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=382,
  serialized_end=442,
)

_SECONDORDERPREDICTIONREQUEST = _descriptor.Descriptor(
  name='SecondOrderPredictionRequest',
  full_name='thermal_model.SecondOrderPredictionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='building', full_name='thermal_model.SecondOrderPredictionRequest.building', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zone', full_name='thermal_model.SecondOrderPredictionRequest.zone', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='current_time', full_name='thermal_model.SecondOrderPredictionRequest.current_time', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action', full_name='thermal_model.SecondOrderPredictionRequest.action', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='indoor_temperature', full_name='thermal_model.SecondOrderPredictionRequest.indoor_temperature', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='previous_indoor_temperature', full_name='thermal_model.SecondOrderPredictionRequest.previous_indoor_temperature', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outside_temperature', full_name='thermal_model.SecondOrderPredictionRequest.outside_temperature', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='other_zone_temperatures', full_name='thermal_model.SecondOrderPredictionRequest.other_zone_temperatures', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature_unit', full_name='thermal_model.SecondOrderPredictionRequest.temperature_unit', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SECONDORDERPREDICTIONREQUEST_OTHERZONETEMPERATURESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=55,
  serialized_end=442,
)


_ERRORREQUEST = _descriptor.Descriptor(
  name='ErrorRequest',
  full_name='thermal_model.ErrorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='building', full_name='thermal_model.ErrorRequest.building', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zone', full_name='thermal_model.ErrorRequest.zone', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action', full_name='thermal_model.ErrorRequest.action', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='thermal_model.ErrorRequest.start', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='thermal_model.ErrorRequest.end', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unit', full_name='thermal_model.ErrorRequest.unit', index=5,
      number=6, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=444,
  serialized_end=548,
)


_PREDICTEDTEMPERATUREREPLY = _descriptor.Descriptor(
  name='PredictedTemperatureReply',
  full_name='thermal_model.PredictedTemperatureReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='thermal_model.PredictedTemperatureReply.time', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature', full_name='thermal_model.PredictedTemperatureReply.temperature', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unit', full_name='thermal_model.PredictedTemperatureReply.unit', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=550,
  serialized_end=626,
)


_ERRORREPLY = _descriptor.Descriptor(
  name='ErrorReply',
  full_name='thermal_model.ErrorReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mean', full_name='thermal_model.ErrorReply.mean', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='var', full_name='thermal_model.ErrorReply.var', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unit', full_name='thermal_model.ErrorReply.unit', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=628,
  serialized_end=681,
)

_SECONDORDERPREDICTIONREQUEST_OTHERZONETEMPERATURESENTRY.containing_type = _SECONDORDERPREDICTIONREQUEST
_SECONDORDERPREDICTIONREQUEST.fields_by_name['other_zone_temperatures'].message_type = _SECONDORDERPREDICTIONREQUEST_OTHERZONETEMPERATURESENTRY
DESCRIPTOR.message_types_by_name['SecondOrderPredictionRequest'] = _SECONDORDERPREDICTIONREQUEST
DESCRIPTOR.message_types_by_name['ErrorRequest'] = _ERRORREQUEST
DESCRIPTOR.message_types_by_name['PredictedTemperatureReply'] = _PREDICTEDTEMPERATUREREPLY
DESCRIPTOR.message_types_by_name['ErrorReply'] = _ERRORREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SecondOrderPredictionRequest = _reflection.GeneratedProtocolMessageType('SecondOrderPredictionRequest', (_message.Message,), dict(

  OtherZoneTemperaturesEntry = _reflection.GeneratedProtocolMessageType('OtherZoneTemperaturesEntry', (_message.Message,), dict(
    DESCRIPTOR = _SECONDORDERPREDICTIONREQUEST_OTHERZONETEMPERATURESENTRY,
    __module__ = 'indoor_temperature_prediction_pb2'
    # @@protoc_insertion_point(class_scope:thermal_model.SecondOrderPredictionRequest.OtherZoneTemperaturesEntry)
    ))
  ,
  DESCRIPTOR = _SECONDORDERPREDICTIONREQUEST,
  __module__ = 'indoor_temperature_prediction_pb2'
  # @@protoc_insertion_point(class_scope:thermal_model.SecondOrderPredictionRequest)
  ))
_sym_db.RegisterMessage(SecondOrderPredictionRequest)
_sym_db.RegisterMessage(SecondOrderPredictionRequest.OtherZoneTemperaturesEntry)

ErrorRequest = _reflection.GeneratedProtocolMessageType('ErrorRequest', (_message.Message,), dict(
  DESCRIPTOR = _ERRORREQUEST,
  __module__ = 'indoor_temperature_prediction_pb2'
  # @@protoc_insertion_point(class_scope:thermal_model.ErrorRequest)
  ))
_sym_db.RegisterMessage(ErrorRequest)

PredictedTemperatureReply = _reflection.GeneratedProtocolMessageType('PredictedTemperatureReply', (_message.Message,), dict(
  DESCRIPTOR = _PREDICTEDTEMPERATUREREPLY,
  __module__ = 'indoor_temperature_prediction_pb2'
  # @@protoc_insertion_point(class_scope:thermal_model.PredictedTemperatureReply)
  ))
_sym_db.RegisterMessage(PredictedTemperatureReply)

ErrorReply = _reflection.GeneratedProtocolMessageType('ErrorReply', (_message.Message,), dict(
  DESCRIPTOR = _ERRORREPLY,
  __module__ = 'indoor_temperature_prediction_pb2'
  # @@protoc_insertion_point(class_scope:thermal_model.ErrorReply)
  ))
_sym_db.RegisterMessage(ErrorReply)


DESCRIPTOR._options = None
_SECONDORDERPREDICTIONREQUEST_OTHERZONETEMPERATURESENTRY._options = None

_INDOORTEMPERATUREPREDICTION = _descriptor.ServiceDescriptor(
  name='IndoorTemperaturePrediction',
  full_name='thermal_model.IndoorTemperaturePrediction',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=684,
  serialized_end=911,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetSecondOrderPrediction',
    full_name='thermal_model.IndoorTemperaturePrediction.GetSecondOrderPrediction',
    index=0,
    containing_service=None,
    input_type=_SECONDORDERPREDICTIONREQUEST,
    output_type=_PREDICTEDTEMPERATUREREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetSecondOrderError',
    full_name='thermal_model.IndoorTemperaturePrediction.GetSecondOrderError',
    index=1,
    containing_service=None,
    input_type=_ERRORREQUEST,
    output_type=_ERRORREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_INDOORTEMPERATUREPREDICTION)

DESCRIPTOR.services_by_name['IndoorTemperaturePrediction'] = _INDOORTEMPERATUREPREDICTION

# @@protoc_insertion_point(module_scope)
