# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/stats/events.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ...api import player_id_pb2
from ...api.stats import extra_mode_stats_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='api/stats/events.proto',
  package='api.stats',
  serialized_pb=_b('\n\x16\x61pi/stats/events.proto\x12\tapi.stats\x1a\x13\x61pi/player_id.proto\x1a api/stats/extra_mode_stats.proto\"7\n\x08\x42\x61llData\x12\r\n\x05pos_x\x18\x01 \x01(\x02\x12\r\n\x05pos_y\x18\x02 \x01(\x02\x12\r\n\x05pos_z\x18\x03 \x01(\x02\"\xfb\x03\n\x03Hit\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12 \n\tplayer_id\x18\x02 \x01(\x0b\x32\r.api.PlayerId\x12\x1a\n\x12\x63ollision_distance\x18\x03 \x01(\x02\x12&\n\tball_data\x18\x04 \x01(\x0b\x32\x13.api.stats.BallData\x12\r\n\x05pass_\x18\x05 \x01(\x08\x12\x0e\n\x06passed\x18\x06 \x01(\x08\x12\x0f\n\x07\x64ribble\x18\x07 \x01(\x08\x12\x1c\n\x14\x64ribble_continuation\x18\x08 \x01(\x08\x12\x0c\n\x04shot\x18\t \x01(\x08\x12\x0c\n\x04goal\x18\n \x01(\x08\x12\x0e\n\x06\x61ssist\x18\x0c \x01(\x08\x12\x10\n\x08\x61ssisted\x18\r \x01(\x08\x12\x0c\n\x04save\x18\x0e \x01(\x08\x12\x0e\n\x06\x61\x65rial\x18\x0f \x01(\x08\x12\x11\n\ton_ground\x18\x10 \x01(\x08\x12\x10\n\x08\x64istance\x18\x11 \x01(\x02\x12\x18\n\x10\x64istance_to_goal\x18\x12 \x01(\x02\x12!\n\x19previous_hit_frame_number\x18\x13 \x01(\x05\x12\x1d\n\x15next_hit_frame_number\x18\x14 \x01(\x05\x12\x13\n\x0bgoal_number\x18\x15 \x01(\x05\x12\x12\n\nis_kickoff\x18\x16 \x01(\x08\x12$\n\x1c\x44\x45PRECATED_field_goal_number\x18\x0b \x01(\x08\"s\n\x04\x42ump\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12\"\n\x0b\x61ttacker_id\x18\x02 \x01(\x0b\x32\r.api.PlayerId\x12 \n\tvictim_id\x18\x03 \x01(\x0b\x32\r.api.PlayerId\x12\x0f\n\x07is_demo\x18\x04 \x01(\x08\"\xb1\x01\n\x0c\x43\x61meraChange\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12 \n\tplayer_id\x18\x02 \x01(\x0b\x32\r.api.PlayerId\x12\x1a\n\x12\x64istance_from_ball\x18\x03 \x01(\x02\x12\x18\n\x10is_in_possession\x18\x04 \x01(\x08\x12\x1b\n\x13length_in_this_mode\x18\x05 \x01(\x02\x12\x16\n\x0eis_on_ball_cam\x18\x06 \x01(\x08\"}\n\nFiftyFifty\x12\x14\n\x0c\x66rame_number\x18\x01 \x01(\x05\x12\x1e\n\x07players\x18\x02 \x03(\x0b\x32\r.api.PlayerId\x12\x12\n\nis_kickoff\x18\x03 \x01(\x08\x12%\n\x0ewinning_player\x18\x04 \x01(\x0b\x32\r.api.PlayerId\"?\n\x07Kickoff\x12\x1a\n\x12start_frame_number\x18\x01 \x01(\x05\x12\x18\n\x10\x65nd_frame_number\x18\x02 \x01(\x05\"\xaf\x01\n\x0fRumbleItemEvent\x12\x18\n\x10\x66rame_number_get\x18\x01 \x01(\x05\x12\x1c\n\x10\x66rame_number_use\x18\x02 \x01(\x05:\x02-1\x12 \n\x04item\x18\x03 \x01(\x0e\x32\x12.api.stats.PowerUp\x12 \n\tplayer_id\x18\x04 \x01(\x0b\x32\r.api.PlayerId\x12 \n\tvictim_id\x18\x05 \x01(\x0b\x32\r.api.PlayerId')
  ,
  dependencies=[player_id_pb2.DESCRIPTOR,extra_mode_stats_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BALLDATA = _descriptor.Descriptor(
  name='BallData',
  full_name='api.stats.BallData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pos_x', full_name='api.stats.BallData.pos_x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pos_y', full_name='api.stats.BallData.pos_y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pos_z', full_name='api.stats.BallData.pos_z', index=2,
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
  serialized_start=92,
  serialized_end=147,
)


_HIT = _descriptor.Descriptor(
  name='Hit',
  full_name='api.stats.Hit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='api.stats.Hit.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_id', full_name='api.stats.Hit.player_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='collision_distance', full_name='api.stats.Hit.collision_distance', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ball_data', full_name='api.stats.Hit.ball_data', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pass_', full_name='api.stats.Hit.pass_', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='passed', full_name='api.stats.Hit.passed', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dribble', full_name='api.stats.Hit.dribble', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dribble_continuation', full_name='api.stats.Hit.dribble_continuation', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shot', full_name='api.stats.Hit.shot', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='goal', full_name='api.stats.Hit.goal', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='assist', full_name='api.stats.Hit.assist', index=10,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='assisted', full_name='api.stats.Hit.assisted', index=11,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='save', full_name='api.stats.Hit.save', index=12,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aerial', full_name='api.stats.Hit.aerial', index=13,
      number=15, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='on_ground', full_name='api.stats.Hit.on_ground', index=14,
      number=16, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distance', full_name='api.stats.Hit.distance', index=15,
      number=17, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distance_to_goal', full_name='api.stats.Hit.distance_to_goal', index=16,
      number=18, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='previous_hit_frame_number', full_name='api.stats.Hit.previous_hit_frame_number', index=17,
      number=19, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='next_hit_frame_number', full_name='api.stats.Hit.next_hit_frame_number', index=18,
      number=20, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='goal_number', full_name='api.stats.Hit.goal_number', index=19,
      number=21, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_kickoff', full_name='api.stats.Hit.is_kickoff', index=20,
      number=22, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='DEPRECATED_field_goal_number', full_name='api.stats.Hit.DEPRECATED_field_goal_number', index=21,
      number=11, type=8, cpp_type=7, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=150,
  serialized_end=657,
)


_BUMP = _descriptor.Descriptor(
  name='Bump',
  full_name='api.stats.Bump',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='api.stats.Bump.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='attacker_id', full_name='api.stats.Bump.attacker_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='victim_id', full_name='api.stats.Bump.victim_id', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_demo', full_name='api.stats.Bump.is_demo', index=3,
      number=4, type=8, cpp_type=7, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=659,
  serialized_end=774,
)


_CAMERACHANGE = _descriptor.Descriptor(
  name='CameraChange',
  full_name='api.stats.CameraChange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='api.stats.CameraChange.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_id', full_name='api.stats.CameraChange.player_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distance_from_ball', full_name='api.stats.CameraChange.distance_from_ball', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_in_possession', full_name='api.stats.CameraChange.is_in_possession', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='length_in_this_mode', full_name='api.stats.CameraChange.length_in_this_mode', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_on_ball_cam', full_name='api.stats.CameraChange.is_on_ball_cam', index=5,
      number=6, type=8, cpp_type=7, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=777,
  serialized_end=954,
)


_FIFTYFIFTY = _descriptor.Descriptor(
  name='FiftyFifty',
  full_name='api.stats.FiftyFifty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number', full_name='api.stats.FiftyFifty.frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='players', full_name='api.stats.FiftyFifty.players', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_kickoff', full_name='api.stats.FiftyFifty.is_kickoff', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='winning_player', full_name='api.stats.FiftyFifty.winning_player', index=3,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=956,
  serialized_end=1081,
)


_KICKOFF = _descriptor.Descriptor(
  name='Kickoff',
  full_name='api.stats.Kickoff',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start_frame_number', full_name='api.stats.Kickoff.start_frame_number', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_frame_number', full_name='api.stats.Kickoff.end_frame_number', index=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1083,
  serialized_end=1146,
)


_RUMBLEITEMEVENT = _descriptor.Descriptor(
  name='RumbleItemEvent',
  full_name='api.stats.RumbleItemEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_number_get', full_name='api.stats.RumbleItemEvent.frame_number_get', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frame_number_use', full_name='api.stats.RumbleItemEvent.frame_number_use', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item', full_name='api.stats.RumbleItemEvent.item', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_id', full_name='api.stats.RumbleItemEvent.player_id', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='victim_id', full_name='api.stats.RumbleItemEvent.victim_id', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1149,
  serialized_end=1324,
)

_HIT.fields_by_name['player_id'].message_type = player_id_pb2._PLAYERID
_HIT.fields_by_name['ball_data'].message_type = _BALLDATA
_BUMP.fields_by_name['attacker_id'].message_type = player_id_pb2._PLAYERID
_BUMP.fields_by_name['victim_id'].message_type = player_id_pb2._PLAYERID
_CAMERACHANGE.fields_by_name['player_id'].message_type = player_id_pb2._PLAYERID
_FIFTYFIFTY.fields_by_name['players'].message_type = player_id_pb2._PLAYERID
_FIFTYFIFTY.fields_by_name['winning_player'].message_type = player_id_pb2._PLAYERID
_RUMBLEITEMEVENT.fields_by_name['item'].enum_type = extra_mode_stats_pb2._POWERUP
_RUMBLEITEMEVENT.fields_by_name['player_id'].message_type = player_id_pb2._PLAYERID
_RUMBLEITEMEVENT.fields_by_name['victim_id'].message_type = player_id_pb2._PLAYERID
DESCRIPTOR.message_types_by_name['BallData'] = _BALLDATA
DESCRIPTOR.message_types_by_name['Hit'] = _HIT
DESCRIPTOR.message_types_by_name['Bump'] = _BUMP
DESCRIPTOR.message_types_by_name['CameraChange'] = _CAMERACHANGE
DESCRIPTOR.message_types_by_name['FiftyFifty'] = _FIFTYFIFTY
DESCRIPTOR.message_types_by_name['Kickoff'] = _KICKOFF
DESCRIPTOR.message_types_by_name['RumbleItemEvent'] = _RUMBLEITEMEVENT

BallData = _reflection.GeneratedProtocolMessageType('BallData', (_message.Message,), dict(
  DESCRIPTOR = _BALLDATA,
  __module__ = 'api.stats.events_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.BallData)
  ))
_sym_db.RegisterMessage(BallData)

Hit = _reflection.GeneratedProtocolMessageType('Hit', (_message.Message,), dict(
  DESCRIPTOR = _HIT,
  __module__ = 'api.stats.events_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.Hit)
  ))
_sym_db.RegisterMessage(Hit)

Bump = _reflection.GeneratedProtocolMessageType('Bump', (_message.Message,), dict(
  DESCRIPTOR = _BUMP,
  __module__ = 'api.stats.events_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.Bump)
  ))
_sym_db.RegisterMessage(Bump)

CameraChange = _reflection.GeneratedProtocolMessageType('CameraChange', (_message.Message,), dict(
  DESCRIPTOR = _CAMERACHANGE,
  __module__ = 'api.stats.events_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.CameraChange)
  ))
_sym_db.RegisterMessage(CameraChange)

FiftyFifty = _reflection.GeneratedProtocolMessageType('FiftyFifty', (_message.Message,), dict(
  DESCRIPTOR = _FIFTYFIFTY,
  __module__ = 'api.stats.events_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.FiftyFifty)
  ))
_sym_db.RegisterMessage(FiftyFifty)

Kickoff = _reflection.GeneratedProtocolMessageType('Kickoff', (_message.Message,), dict(
  DESCRIPTOR = _KICKOFF,
  __module__ = 'api.stats.events_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.Kickoff)
  ))
_sym_db.RegisterMessage(Kickoff)

RumbleItemEvent = _reflection.GeneratedProtocolMessageType('RumbleItemEvent', (_message.Message,), dict(
  DESCRIPTOR = _RUMBLEITEMEVENT,
  __module__ = 'api.stats.events_pb2'
  # @@protoc_insertion_point(class_scope:api.stats.RumbleItemEvent)
  ))
_sym_db.RegisterMessage(RumbleItemEvent)


# @@protoc_insertion_point(module_scope)
