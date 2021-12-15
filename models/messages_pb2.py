# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0emessages.proto\"Q\n\x04\x66ile\x12\n\n\x02id\x18\x01 \x01(\r\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\x0c\n\x04size\x18\x03 \x01(\x04\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x0f\n\x07\x63reated\x18\x05 \x01(\x04\"9\n\x16\x62roadcast_request_file\x12\x11\n\tfilenames\x18\x01 \x03(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"Y\n\x17\x62roadcast_response_node\x12\x0c\n\x04node\x18\x01 \x01(\t\x12\x11\n\tfilenames\x18\x02 \x03(\t\x12\x0f\n\x07hasFile\x18\x03 \x01(\x08\x12\x0c\n\x04type\x18\x04 \x01(\t\"L\n\x1a\x62roadcast_request_specefic\x12\r\n\x05nodes\x18\x01 \x03(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x11\n\tfilenames\x18\x04 \x03(\tb\x06proto3'
)




_FILE = _descriptor.Descriptor(
  name='file',
  full_name='file',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='file.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filename', full_name='file.filename', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='file.size', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='file.type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created', full_name='file.created', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=18,
  serialized_end=99,
)


_BROADCAST_REQUEST_FILE = _descriptor.Descriptor(
  name='broadcast_request_file',
  full_name='broadcast_request_file',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filenames', full_name='broadcast_request_file.filenames', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='broadcast_request_file.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=101,
  serialized_end=158,
)


_BROADCAST_RESPONSE_NODE = _descriptor.Descriptor(
  name='broadcast_response_node',
  full_name='broadcast_response_node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node', full_name='broadcast_response_node.node', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filenames', full_name='broadcast_response_node.filenames', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hasFile', full_name='broadcast_response_node.hasFile', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='broadcast_response_node.type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=160,
  serialized_end=249,
)


_BROADCAST_REQUEST_SPECEFIC = _descriptor.Descriptor(
  name='broadcast_request_specefic',
  full_name='broadcast_request_specefic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nodes', full_name='broadcast_request_specefic.nodes', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='broadcast_request_specefic.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filenames', full_name='broadcast_request_specefic.filenames', index=2,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=251,
  serialized_end=327,
)

DESCRIPTOR.message_types_by_name['file'] = _FILE
DESCRIPTOR.message_types_by_name['broadcast_request_file'] = _BROADCAST_REQUEST_FILE
DESCRIPTOR.message_types_by_name['broadcast_response_node'] = _BROADCAST_RESPONSE_NODE
DESCRIPTOR.message_types_by_name['broadcast_request_specefic'] = _BROADCAST_REQUEST_SPECEFIC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

file = _reflection.GeneratedProtocolMessageType('file', (_message.Message,), {
  'DESCRIPTOR' : _FILE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:file)
  })
_sym_db.RegisterMessage(file)

broadcast_request_file = _reflection.GeneratedProtocolMessageType('broadcast_request_file', (_message.Message,), {
  'DESCRIPTOR' : _BROADCAST_REQUEST_FILE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:broadcast_request_file)
  })
_sym_db.RegisterMessage(broadcast_request_file)

broadcast_response_node = _reflection.GeneratedProtocolMessageType('broadcast_response_node', (_message.Message,), {
  'DESCRIPTOR' : _BROADCAST_RESPONSE_NODE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:broadcast_response_node)
  })
_sym_db.RegisterMessage(broadcast_response_node)

broadcast_request_specefic = _reflection.GeneratedProtocolMessageType('broadcast_request_specefic', (_message.Message,), {
  'DESCRIPTOR' : _BROADCAST_REQUEST_SPECEFIC,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:broadcast_request_specefic)
  })
_sym_db.RegisterMessage(broadcast_request_specefic)


# @@protoc_insertion_point(module_scope)
