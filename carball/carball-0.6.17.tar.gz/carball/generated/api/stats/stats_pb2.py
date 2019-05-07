# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/stats/stats.proto

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
  name='api/stats/stats.proto',
  package='api.stats',
  serialized_pb=_b('\n\x15\x61pi/stats/stats.proto\x12\tapi.stats\"\x8e\x01\n\nPossession\x12\x17\n\x0fpossession_time\x18\x01 \x01(\x01\x12\x11\n\tturnovers\x18\x02 \x01(\x05\x12\x1c\n\x14turnovers_on_my_half\x18\x03 \x01(\x05\x12\x1f\n\x17turnovers_on_their_half\x18\x04 \x01(\x05\x12\x15\n\rwon_turnovers\x18\x05 \x01(\x05\"\xe8\x02\n\x14PositionalTendencies\x12\x16\n\x0etime_on_ground\x18\x01 \x01(\x02\x12\x17\n\x0ftime_low_in_air\x18\x02 \x01(\x02\x12\x18\n\x10time_high_in_air\x18\x03 \x01(\x02\x12\x1e\n\x16time_in_defending_half\x18\x04 \x01(\x02\x12\x1e\n\x16time_in_attacking_half\x18\x05 \x01(\x02\x12\x1f\n\x17time_in_defending_third\x18\x06 \x01(\x02\x12\x1d\n\x15time_in_neutral_third\x18\x07 \x01(\x02\x12\x1f\n\x17time_in_attacking_third\x18\x08 \x01(\x02\x12\x18\n\x10time_behind_ball\x18\t \x01(\x02\x12\x1a\n\x12time_in_front_ball\x18\n \x01(\x02\x12\x16\n\x0etime_near_wall\x18\x0b \x01(\x02\x12\x16\n\x0etime_in_corner\x18\x0c \x01(\x02\"e\n\x08\x41verages\x12\x15\n\raverage_speed\x18\x01 \x01(\x02\x12\x1c\n\x14\x61verage_hit_distance\x18\x02 \x01(\x02\x12$\n\x1c\x61verage_distance_from_center\x18\x03 \x01(\x02\"\xc0\x01\n\tHitCounts\x12\x12\n\ntotal_hits\x18\x01 \x01(\x05\x12\x13\n\x0btotal_goals\x18\x02 \x01(\x05\x12\x14\n\x0ctotal_passes\x18\x03 \x01(\x05\x12\x13\n\x0btotal_saves\x18\x04 \x01(\x05\x12\x13\n\x0btotal_shots\x18\x05 \x01(\x05\x12\x16\n\x0etotal_dribbles\x18\x06 \x01(\x05\x12\x1b\n\x13total_dribble_conts\x18\x07 \x01(\x05\x12\x15\n\rtotal_aerials\x18\x08 \x01(\x05\"]\n\x05Speed\x12\x1a\n\x12time_at_slow_speed\x18\x01 \x01(\x02\x12\x1b\n\x13time_at_super_sonic\x18\x02 \x01(\x02\x12\x1b\n\x13time_at_boost_speed\x18\x03 \x01(\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_POSSESSION = _descriptor.Descriptor(
  name='Possession',
  full_name='api.stats.Possession',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='possession_time', full_name='api.stats.Possession.possession_time', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='turnovers', full_name='api.stats.Possession.turnovers', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='turnovers_on_my_half', full_name='api.stats.Possession.turnovers_on_my_half', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='turnovers_on_their_half', full_name='api.stats.Possession.turnovers_on_their_half', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='won_turnovers', full_name='api.stats.Possession.won_turnovers', index=4,
      number=5, type=5, cpp_type=1, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=179,
)


_POSITIONALTENDENCIES = _descriptor.Descriptor(
  name='PositionalTendencies',
  full_name='api.stats.PositionalTendencies',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time_on_ground', full_name='api.stats.PositionalTendencies.time_on_ground', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_low_in_air', full_name='api.stats.PositionalTendencies.time_low_in_air', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_high_in_air', full_name='api.stats.PositionalTendencies.time_high_in_air', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_in_defending_half', full_name='api.stats.PositionalTendencies.time_in_defending_half', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_in_attacking_half', full_name='api.stats.PositionalTendencies.time_in_attacking_half', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_in_defending_third', full_name='api.stats.PositionalTendencies.time_in_defending_third', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_in_neutral_third', full_name='api.stats.PositionalTendencies.time_in_neutral_third', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_in_attacking_third', full_name='api.stats.PositionalTendencies.time_in_attacking_third', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_behind_ball', full_name='api.stats.PositionalTendencies.time_behind_ball', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_in_front_ball', full_name='api.stats.PositionalTendencies.time_in_front_ball', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_near_wall', full_name='api.stats.PositionalTendencies.time_near_wall', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_in_corner', full_name='api.stats.PositionalTendencies.time_in_corner', index=11,
      number=12, type=2, cpp_type=6, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=182,
  serialized_end=542,
)


_AVERAGES = _descriptor.Descriptor(
  name='Averages',
  full_name='api.stats.Averages',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='average_speed', full_name='api.stats.Averages.average_speed', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='average_hit_distance', full_name='api.stats.Averages.average_hit_distance', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='average_distance_from_center', full_name='api.stats.Averages.average_distance_from_center', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=544,
  serialized_end=645,
)


_HITCOUNTS = _descriptor.Descriptor(
  name='HitCounts',
  full_name='api.stats.HitCounts',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='total_hits', full_name='api.stats.HitCounts.total_hits', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_goals', full_name='api.stats.HitCounts.total_goals', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_passes', full_name='api.stats.HitCounts.total_passes', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_saves', full_name='api.stats.HitCounts.total_saves', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_shots', full_name='api.stats.HitCounts.total_shots', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_dribbles', full_name='api.stats.HitCounts.total_dribbles', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_dribble_conts', full_name='api.stats.HitCounts.total_dribble_conts', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_aerials', full_name='api.stats.HitCounts.total_aerials', index=7,
      number=8, type=5, cpp_type=1, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=648,
  serialized_end=840,
)


_SPEED = _descriptor.Descriptor(
  name='Speed',
  full_name='api.stats.Speed',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time_at_slow_speed', full_name='api.stats.Speed.time_at_slow_speed', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_at_super_sonic', full_name='api.stats.Speed.time_at_super_sonic', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_at_boost_speed', full_name='api.stats.Speed.time_at_boost_speed', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=842,
  serialized_end=935,
)

DESCRIPTOR.message_types_by_name['Possession'] = _POSSESSION
DESCRIPTOR.message_types_by_name['PositionalTendencies'] = _POSITIONALTENDENCIES
DESCRIPTOR.message_types_by_name['Averages'] = _AVERAGES
DESCRIPTOR.message_types_by_name['HitCounts'] = _HITCOUNTS
DESCRIPTOR.message_types_by_name['Speed'] = _SPEED

Possession = _reflection.GeneratedProtocolMessageType('Possession', (_message.Message,), dict(
  DESCRIPTOR = _POSSESSION,
  __module__ = 'api.stats.stats_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.Possession)
  ))
_sym_db.RegisterMessage(Possession)

PositionalTendencies = _reflection.GeneratedProtocolMessageType('PositionalTendencies', (_message.Message,), dict(
  DESCRIPTOR = _POSITIONALTENDENCIES,
  __module__ = 'api.stats.stats_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.PositionalTendencies)
  ))
_sym_db.RegisterMessage(PositionalTendencies)

Averages = _reflection.GeneratedProtocolMessageType('Averages', (_message.Message,), dict(
  DESCRIPTOR = _AVERAGES,
  __module__ = 'api.stats.stats_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.Averages)
  ))
_sym_db.RegisterMessage(Averages)

HitCounts = _reflection.GeneratedProtocolMessageType('HitCounts', (_message.Message,), dict(
  DESCRIPTOR = _HITCOUNTS,
  __module__ = 'api.stats.stats_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.HitCounts)
  ))
_sym_db.RegisterMessage(HitCounts)

Speed = _reflection.GeneratedProtocolMessageType('Speed', (_message.Message,), dict(
  DESCRIPTOR = _SPEED,
  __module__ = 'api.stats.stats_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.Speed)
  ))
_sym_db.RegisterMessage(Speed)


# @@protoc_insertion_point(module_scope)
