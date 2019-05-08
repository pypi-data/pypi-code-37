# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='status.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0cstatus.proto\"\x90\x0e\n\x06Status\x12\n\n\x02sn\x18\x01 \x01(\t\x12\x1a\n\x04site\x18\x02 \x01(\x0b\x32\x0c.Status.Site\x12\x11\n\tpowerWatt\x18\x03 \x01(\x02\x12\x0f\n\x07voltage\x18\x04 \x01(\x02\x12\x13\n\x0b\x66requencyHz\x18\x05 \x01(\x02\x12\x32\n\x10optimizersStatus\x18\x06 \x01(\x0b\x32\x18.Status.OptimizersStatus\x12\x0b\n\x03sOk\x18\x07 \x01(\x08\x12%\n\x06status\x18\x08 \x01(\x0e\x32\x15.Status.ManagerStatus\x12\x14\n\x0cswitchStatus\x18\t \x01(\t\x12\x0e\n\x06\x63osPhi\x18\n \x01(\x02\x12\x12\n\npowerLimit\x18\x0b \x01(\x02\x12\x0f\n\x07\x63ountry\x18\x0c \x01(\x05\x12$\n\tinverters\x18\r \x01(\x0b\x32\x11.Status.Inverters\x12,\n\rcommunication\x18\x0e \x01(\x0b\x32\x15.Status.Communication\x12(\n\x06\x65nergy\x18\x0f \x01(\x0b\x32\x18.Status.EnergyStatistics\x12\x17\n\x0fportiaErrorCode\x18\x10 \x01(\t\x12\x17\n\x0fportiaSubsystem\x18\x11 \x01(\t\x12\x1c\n\x05\x65vese\x18\x12 \x01(\x0b\x32\r.Status.Evese\x12!\n\nmetersList\x18\x13 \x03(\x0b\x32\r.Status.Meter\x12&\n\rbatteriesList\x18\x14 \x03(\x0b\x32\x0f.Status.Battery\x12*\n\x0cnotification\x18\x15 \x01(\x0b\x32\x14.Status.Notification\x12/\n\nserverComm\x18\x16 \x01(\x0b\x32\x1b.Status.ServerCommunication\x1a\xa0\x01\n\x04Site\x12\x16\n\x0eproductionWatt\x18\x01 \x01(\x02\x12\x15\n\rsizeLimitWatt\x18\x02 \x01(\x02\x12\x33\n\x0einverterStatus\x18\x03 \x01(\x0b\x32\x1b.Status.Site.InverterStatus\x1a\x34\n\x0eInverterStatus\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\t\x12\x11\n\tconnected\x18\x02 \x01(\t\x1a\x31\n\x10OptimizersStatus\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0e\n\x06online\x18\x02 \x01(\x05\x1a\xd9\x03\n\tInverters\x12$\n\x04left\x18\x01 \x01(\x0b\x32\x16.Status.Inverters.Unit\x12\'\n\x07primary\x18\x02 \x01(\x0b\x32\x16.Status.Inverters.Unit\x12%\n\x05right\x18\x03 \x01(\x0b\x32\x16.Status.Inverters.Unit\x1a\xd6\x01\n\x04Unit\x12\r\n\x05\x64spSn\x18\x01 \x01(\t\x12\x0f\n\x07voltage\x18\x02 \x01(\x02\x12\x32\n\x10optimizersStatus\x18\x03 \x01(\x0b\x32\x18.Status.OptimizersStatus\x12\x32\n\x0btemperature\x18\x04 \x01(\x0b\x32\x1d.Status.Inverters.Temperature\x12\x0b\n\x03\x66\x61n\x18\x05 \x01(\t\x12\x11\n\terrorCode\x18\x06 \x01(\t\x12\x11\n\tsubSystem\x18\x07 \x01(\t\x12\x13\n\x0b\x62\x61\x64Position\x18\x08 \x01(\t\x1a}\n\x0bTemperature\x12\r\n\x05value\x18\x01 \x01(\x05\x12\x32\n\x05units\x18\x02 \x01(\x0b\x32#.Status.Inverters.Temperature.Units\x1a+\n\x05Units\x12\x0f\n\x07\x63\x65lsius\x18\x01 \x01(\x08\x12\x11\n\tfarenheit\x18\x02 \x01(\x08\x1a\x0f\n\rCommunication\x1aU\n\x10\x45nergyStatistics\x12\r\n\x05today\x18\x01 \x01(\x02\x12\x11\n\tthisMonth\x18\x02 \x01(\x02\x12\x10\n\x08thisYear\x18\x03 \x01(\x02\x12\r\n\x05total\x18\x04 \x01(\x02\x1a\x07\n\x05\x45vese\x1aw\n\x05Meter\x12\x16\n\x0e\x63onnectionType\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\t\x12\x14\n\x0c\x63urrentPower\x18\x05 \x01(\x02\x12\x13\n\x0btotalEnergy\x18\x06 \x01(\x02\x12\x0f\n\x07s0Pulse\x18\x07 \x01(\t\x1a\t\n\x07\x42\x61ttery\x1a\x0e\n\x0cNotification\x1a\x15\n\x13ServerCommunication\"\xad\x01\n\rManagerStatus\x12\x11\n\rSHUTTING_DOWN\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x12\x0b\n\x07STANDBY\x10\x02\x12\x0b\n\x07PAIRING\x10\x03\x12\x14\n\x10POWER_PRODUCTION\x10\x04\x12\x0f\n\x0b\x41\x43_CHARGING\x10\x05\x12\x0e\n\nNOT_PAIRED\x10\x06\x12\x0e\n\nNIGHT_MODE\x10\x07\x12\x13\n\x0fGRID_MONITORING\x10\x08\x12\x08\n\x04IDLE\x10\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_STATUS_MANAGERSTATUS = _descriptor.EnumDescriptor(
  name='ManagerStatus',
  full_name='Status.ManagerStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SHUTTING_DOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STANDBY', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAIRING', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POWER_PRODUCTION', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AC_CHARGING', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_PAIRED', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NIGHT_MODE', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRID_MONITORING', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IDLE', index=9, number=9,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1652,
  serialized_end=1825,
)
_sym_db.RegisterEnumDescriptor(_STATUS_MANAGERSTATUS)


_STATUS_SITE_INVERTERSTATUS = _descriptor.Descriptor(
  name='InverterStatus',
  full_name='Status.Site.InverterStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enabled', full_name='Status.Site.InverterStatus.enabled', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='connected', full_name='Status.Site.InverterStatus.connected', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=786,
  serialized_end=838,
)

_STATUS_SITE = _descriptor.Descriptor(
  name='Site',
  full_name='Status.Site',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='productionWatt', full_name='Status.Site.productionWatt', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sizeLimitWatt', full_name='Status.Site.sizeLimitWatt', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inverterStatus', full_name='Status.Site.inverterStatus', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STATUS_SITE_INVERTERSTATUS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=678,
  serialized_end=838,
)

_STATUS_OPTIMIZERSSTATUS = _descriptor.Descriptor(
  name='OptimizersStatus',
  full_name='Status.OptimizersStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='total', full_name='Status.OptimizersStatus.total', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='online', full_name='Status.OptimizersStatus.online', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=840,
  serialized_end=889,
)

_STATUS_INVERTERS_UNIT = _descriptor.Descriptor(
  name='Unit',
  full_name='Status.Inverters.Unit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dspSn', full_name='Status.Inverters.Unit.dspSn', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='voltage', full_name='Status.Inverters.Unit.voltage', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optimizersStatus', full_name='Status.Inverters.Unit.optimizersStatus', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='temperature', full_name='Status.Inverters.Unit.temperature', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fan', full_name='Status.Inverters.Unit.fan', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='errorCode', full_name='Status.Inverters.Unit.errorCode', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subSystem', full_name='Status.Inverters.Unit.subSystem', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='badPosition', full_name='Status.Inverters.Unit.badPosition', index=7,
      number=8, type=9, cpp_type=9, label=1,
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
  serialized_start=1024,
  serialized_end=1238,
)

_STATUS_INVERTERS_TEMPERATURE_UNITS = _descriptor.Descriptor(
  name='Units',
  full_name='Status.Inverters.Temperature.Units',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='celsius', full_name='Status.Inverters.Temperature.Units.celsius', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='farenheit', full_name='Status.Inverters.Temperature.Units.farenheit', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=1322,
  serialized_end=1365,
)

_STATUS_INVERTERS_TEMPERATURE = _descriptor.Descriptor(
  name='Temperature',
  full_name='Status.Inverters.Temperature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='Status.Inverters.Temperature.value', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='units', full_name='Status.Inverters.Temperature.units', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STATUS_INVERTERS_TEMPERATURE_UNITS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1240,
  serialized_end=1365,
)

_STATUS_INVERTERS = _descriptor.Descriptor(
  name='Inverters',
  full_name='Status.Inverters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='left', full_name='Status.Inverters.left', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='primary', full_name='Status.Inverters.primary', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='right', full_name='Status.Inverters.right', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STATUS_INVERTERS_UNIT, _STATUS_INVERTERS_TEMPERATURE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=892,
  serialized_end=1365,
)

_STATUS_COMMUNICATION = _descriptor.Descriptor(
  name='Communication',
  full_name='Status.Communication',
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
  serialized_start=1367,
  serialized_end=1382,
)

_STATUS_ENERGYSTATISTICS = _descriptor.Descriptor(
  name='EnergyStatistics',
  full_name='Status.EnergyStatistics',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='today', full_name='Status.EnergyStatistics.today', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='thisMonth', full_name='Status.EnergyStatistics.thisMonth', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='thisYear', full_name='Status.EnergyStatistics.thisYear', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total', full_name='Status.EnergyStatistics.total', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=1384,
  serialized_end=1469,
)

_STATUS_EVESE = _descriptor.Descriptor(
  name='Evese',
  full_name='Status.Evese',
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
  serialized_start=1471,
  serialized_end=1478,
)

_STATUS_METER = _descriptor.Descriptor(
  name='Meter',
  full_name='Status.Meter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='connectionType', full_name='Status.Meter.connectionType', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='Status.Meter.status', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='Status.Meter.id', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currentPower', full_name='Status.Meter.currentPower', index=3,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='totalEnergy', full_name='Status.Meter.totalEnergy', index=4,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='s0Pulse', full_name='Status.Meter.s0Pulse', index=5,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=1480,
  serialized_end=1599,
)

_STATUS_BATTERY = _descriptor.Descriptor(
  name='Battery',
  full_name='Status.Battery',
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
  serialized_start=1601,
  serialized_end=1610,
)

_STATUS_NOTIFICATION = _descriptor.Descriptor(
  name='Notification',
  full_name='Status.Notification',
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
  serialized_start=1612,
  serialized_end=1626,
)

_STATUS_SERVERCOMMUNICATION = _descriptor.Descriptor(
  name='ServerCommunication',
  full_name='Status.ServerCommunication',
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
  serialized_start=1628,
  serialized_end=1649,
)

_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sn', full_name='Status.sn', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='site', full_name='Status.site', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='powerWatt', full_name='Status.powerWatt', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='voltage', full_name='Status.voltage', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frequencyHz', full_name='Status.frequencyHz', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='optimizersStatus', full_name='Status.optimizersStatus', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sOk', full_name='Status.sOk', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='Status.status', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='switchStatus', full_name='Status.switchStatus', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cosPhi', full_name='Status.cosPhi', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='powerLimit', full_name='Status.powerLimit', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country', full_name='Status.country', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inverters', full_name='Status.inverters', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='communication', full_name='Status.communication', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='energy', full_name='Status.energy', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='portiaErrorCode', full_name='Status.portiaErrorCode', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='portiaSubsystem', full_name='Status.portiaSubsystem', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='evese', full_name='Status.evese', index=17,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='metersList', full_name='Status.metersList', index=18,
      number=19, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='batteriesList', full_name='Status.batteriesList', index=19,
      number=20, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='notification', full_name='Status.notification', index=20,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='serverComm', full_name='Status.serverComm', index=21,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STATUS_SITE, _STATUS_OPTIMIZERSSTATUS, _STATUS_INVERTERS, _STATUS_COMMUNICATION, _STATUS_ENERGYSTATISTICS, _STATUS_EVESE, _STATUS_METER, _STATUS_BATTERY, _STATUS_NOTIFICATION, _STATUS_SERVERCOMMUNICATION, ],
  enum_types=[
    _STATUS_MANAGERSTATUS,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=1825,
)

_STATUS_SITE_INVERTERSTATUS.containing_type = _STATUS_SITE
_STATUS_SITE.fields_by_name['inverterStatus'].message_type = _STATUS_SITE_INVERTERSTATUS
_STATUS_SITE.containing_type = _STATUS
_STATUS_OPTIMIZERSSTATUS.containing_type = _STATUS
_STATUS_INVERTERS_UNIT.fields_by_name['optimizersStatus'].message_type = _STATUS_OPTIMIZERSSTATUS
_STATUS_INVERTERS_UNIT.fields_by_name['temperature'].message_type = _STATUS_INVERTERS_TEMPERATURE
_STATUS_INVERTERS_UNIT.containing_type = _STATUS_INVERTERS
_STATUS_INVERTERS_TEMPERATURE_UNITS.containing_type = _STATUS_INVERTERS_TEMPERATURE
_STATUS_INVERTERS_TEMPERATURE.fields_by_name['units'].message_type = _STATUS_INVERTERS_TEMPERATURE_UNITS
_STATUS_INVERTERS_TEMPERATURE.containing_type = _STATUS_INVERTERS
_STATUS_INVERTERS.fields_by_name['left'].message_type = _STATUS_INVERTERS_UNIT
_STATUS_INVERTERS.fields_by_name['primary'].message_type = _STATUS_INVERTERS_UNIT
_STATUS_INVERTERS.fields_by_name['right'].message_type = _STATUS_INVERTERS_UNIT
_STATUS_INVERTERS.containing_type = _STATUS
_STATUS_COMMUNICATION.containing_type = _STATUS
_STATUS_ENERGYSTATISTICS.containing_type = _STATUS
_STATUS_EVESE.containing_type = _STATUS
_STATUS_METER.containing_type = _STATUS
_STATUS_BATTERY.containing_type = _STATUS
_STATUS_NOTIFICATION.containing_type = _STATUS
_STATUS_SERVERCOMMUNICATION.containing_type = _STATUS
_STATUS.fields_by_name['site'].message_type = _STATUS_SITE
_STATUS.fields_by_name['optimizersStatus'].message_type = _STATUS_OPTIMIZERSSTATUS
_STATUS.fields_by_name['status'].enum_type = _STATUS_MANAGERSTATUS
_STATUS.fields_by_name['inverters'].message_type = _STATUS_INVERTERS
_STATUS.fields_by_name['communication'].message_type = _STATUS_COMMUNICATION
_STATUS.fields_by_name['energy'].message_type = _STATUS_ENERGYSTATISTICS
_STATUS.fields_by_name['evese'].message_type = _STATUS_EVESE
_STATUS.fields_by_name['metersList'].message_type = _STATUS_METER
_STATUS.fields_by_name['batteriesList'].message_type = _STATUS_BATTERY
_STATUS.fields_by_name['notification'].message_type = _STATUS_NOTIFICATION
_STATUS.fields_by_name['serverComm'].message_type = _STATUS_SERVERCOMMUNICATION
_STATUS_MANAGERSTATUS.containing_type = _STATUS
DESCRIPTOR.message_types_by_name['Status'] = _STATUS

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), dict(

  Site = _reflection.GeneratedProtocolMessageType('Site', (_message.Message,), dict(

    InverterStatus = _reflection.GeneratedProtocolMessageType('InverterStatus', (_message.Message,), dict(
      DESCRIPTOR = _STATUS_SITE_INVERTERSTATUS,
      __module__ = 'status_pb2'
      # @@protoc_insertion_point(class_scope:Status.Site.InverterStatus)
      ))
    ,
    DESCRIPTOR = _STATUS_SITE,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.Site)
    ))
  ,

  OptimizersStatus = _reflection.GeneratedProtocolMessageType('OptimizersStatus', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_OPTIMIZERSSTATUS,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.OptimizersStatus)
    ))
  ,

  Inverters = _reflection.GeneratedProtocolMessageType('Inverters', (_message.Message,), dict(

    Unit = _reflection.GeneratedProtocolMessageType('Unit', (_message.Message,), dict(
      DESCRIPTOR = _STATUS_INVERTERS_UNIT,
      __module__ = 'status_pb2'
      # @@protoc_insertion_point(class_scope:Status.Inverters.Unit)
      ))
    ,

    Temperature = _reflection.GeneratedProtocolMessageType('Temperature', (_message.Message,), dict(

      Units = _reflection.GeneratedProtocolMessageType('Units', (_message.Message,), dict(
        DESCRIPTOR = _STATUS_INVERTERS_TEMPERATURE_UNITS,
        __module__ = 'status_pb2'
        # @@protoc_insertion_point(class_scope:Status.Inverters.Temperature.Units)
        ))
      ,
      DESCRIPTOR = _STATUS_INVERTERS_TEMPERATURE,
      __module__ = 'status_pb2'
      # @@protoc_insertion_point(class_scope:Status.Inverters.Temperature)
      ))
    ,
    DESCRIPTOR = _STATUS_INVERTERS,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.Inverters)
    ))
  ,

  Communication = _reflection.GeneratedProtocolMessageType('Communication', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_COMMUNICATION,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.Communication)
    ))
  ,

  EnergyStatistics = _reflection.GeneratedProtocolMessageType('EnergyStatistics', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_ENERGYSTATISTICS,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.EnergyStatistics)
    ))
  ,

  Evese = _reflection.GeneratedProtocolMessageType('Evese', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_EVESE,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.Evese)
    ))
  ,

  Meter = _reflection.GeneratedProtocolMessageType('Meter', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_METER,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.Meter)
    ))
  ,

  Battery = _reflection.GeneratedProtocolMessageType('Battery', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_BATTERY,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.Battery)
    ))
  ,

  Notification = _reflection.GeneratedProtocolMessageType('Notification', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_NOTIFICATION,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.Notification)
    ))
  ,

  ServerCommunication = _reflection.GeneratedProtocolMessageType('ServerCommunication', (_message.Message,), dict(
    DESCRIPTOR = _STATUS_SERVERCOMMUNICATION,
    __module__ = 'status_pb2'
    # @@protoc_insertion_point(class_scope:Status.ServerCommunication)
    ))
  ,
  DESCRIPTOR = _STATUS,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:Status)
  ))
_sym_db.RegisterMessage(Status)
_sym_db.RegisterMessage(Status.Site)
_sym_db.RegisterMessage(Status.Site.InverterStatus)
_sym_db.RegisterMessage(Status.OptimizersStatus)
_sym_db.RegisterMessage(Status.Inverters)
_sym_db.RegisterMessage(Status.Inverters.Unit)
_sym_db.RegisterMessage(Status.Inverters.Temperature)
_sym_db.RegisterMessage(Status.Inverters.Temperature.Units)
_sym_db.RegisterMessage(Status.Communication)
_sym_db.RegisterMessage(Status.EnergyStatistics)
_sym_db.RegisterMessage(Status.Evese)
_sym_db.RegisterMessage(Status.Meter)
_sym_db.RegisterMessage(Status.Battery)
_sym_db.RegisterMessage(Status.Notification)
_sym_db.RegisterMessage(Status.ServerCommunication)


# @@protoc_insertion_point(module_scope)
