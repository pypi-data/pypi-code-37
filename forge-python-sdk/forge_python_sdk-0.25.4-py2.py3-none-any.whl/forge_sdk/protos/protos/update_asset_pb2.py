# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: update_asset.proto
import sys

from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_b = sys.version_info[0] < 3 and (
    lambda x: x) or (lambda x: x.encode('latin1'))
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name='update_asset.proto',
    package='forge_abi',
    syntax='proto3',
    serialized_options=None,
    serialized_pb=_b('\n\x12update_asset.proto\x12\tforge_abi\x1a\x19google/protobuf/any.proto\"U\n\rUpdateAssetTx\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07moniker\x18\x02 \x01(\t\x12\"\n\x04\x64\x61ta\x18\x0f \x01(\x0b\x32\x14.google.protobuf.Anyb\x06proto3'),
    dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR, ])


_UPDATEASSETTX = _descriptor.Descriptor(
    name='UpdateAssetTx',
    full_name='forge_abi.UpdateAssetTx',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='address', full_name='forge_abi.UpdateAssetTx.address', index=0,
            number=1, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='moniker', full_name='forge_abi.UpdateAssetTx.moniker', index=1,
            number=2, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='data', full_name='forge_abi.UpdateAssetTx.data', index=2,
            number=15, type=11, cpp_type=10, label=1,
            has_default_value=False, default_value=None,
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
    serialized_start=60,
    serialized_end=145,
)

_UPDATEASSETTX.fields_by_name['data'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['UpdateAssetTx'] = _UPDATEASSETTX
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UpdateAssetTx = _reflection.GeneratedProtocolMessageType('UpdateAssetTx', (_message.Message,), dict(
    DESCRIPTOR=_UPDATEASSETTX,
    __module__='update_asset_pb2'
    # @@protoc_insertion_point(class_scope:forge_abi.UpdateAssetTx)
))
_sym_db.RegisterMessage(UpdateAssetTx)


# @@protoc_insertion_point(module_scope)
