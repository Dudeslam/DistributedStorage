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
  serialized_pb=b'\n\x0emessages.proto\"&\n\x04\x66ile\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"#\n\x0fgetdata_request\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"0\n\rdelegate_file\x12\x11\n\tfilenames\x18\x01 \x03(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"M\n\x15\x64\x65legate_erasure_file\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x14\n\x0cmax_erasures\x18\x03 \x01(\x05\"Q\n\x19\x64\x65legate_get_erasure_file\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x14\n\x0cmax_erasures\x18\x03 \x01(\x05\"9\n\x16\x62roadcast_request_file\x12\x11\n\tfilenames\x18\x01 \x03(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"Y\n\x17\x62roadcast_response_node\x12\x0c\n\x04node\x18\x01 \x01(\t\x12\x11\n\tfilenames\x18\x02 \x03(\t\x12\x0f\n\x07hasFile\x18\x03 \x01(\x08\x12\x0c\n\x04type\x18\x04 \x01(\t\"L\n\x1a\x62roadcast_request_specefic\x12\r\n\x05nodes\x18\x01 \x03(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x11\n\tfilenames\x18\x04 \x03(\t\"<\n\x1a\x62roadcast_request_fragment\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"/\n\x1aworker_store_file_response\x12\x11\n\tfragments\x18\x01 \x03(\tb\x06proto3'
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
      name='filename', full_name='file.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='file.type', index=1,
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
  serialized_start=18,
  serialized_end=56,
)


_GETDATA_REQUEST = _descriptor.Descriptor(
  name='getdata_request',
  full_name='getdata_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='getdata_request.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=58,
  serialized_end=93,
)


_DELEGATE_FILE = _descriptor.Descriptor(
  name='delegate_file',
  full_name='delegate_file',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filenames', full_name='delegate_file.filenames', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='delegate_file.type', index=1,
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
  serialized_start=95,
  serialized_end=143,
)


_DELEGATE_ERASURE_FILE = _descriptor.Descriptor(
  name='delegate_erasure_file',
  full_name='delegate_erasure_file',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='delegate_erasure_file.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='delegate_erasure_file.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_erasures', full_name='delegate_erasure_file.max_erasures', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=145,
  serialized_end=222,
)


_DELEGATE_GET_ERASURE_FILE = _descriptor.Descriptor(
  name='delegate_get_erasure_file',
  full_name='delegate_get_erasure_file',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='delegate_get_erasure_file.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='delegate_get_erasure_file.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_erasures', full_name='delegate_get_erasure_file.max_erasures', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=224,
  serialized_end=305,
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
  serialized_start=307,
  serialized_end=364,
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
  serialized_start=366,
  serialized_end=455,
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
  serialized_start=457,
  serialized_end=533,
)


_BROADCAST_REQUEST_FRAGMENT = _descriptor.Descriptor(
  name='broadcast_request_fragment',
  full_name='broadcast_request_fragment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='broadcast_request_fragment.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='broadcast_request_fragment.type', index=1,
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
  serialized_start=535,
  serialized_end=595,
)


_WORKER_STORE_FILE_RESPONSE = _descriptor.Descriptor(
  name='worker_store_file_response',
  full_name='worker_store_file_response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='fragments', full_name='worker_store_file_response.fragments', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=597,
  serialized_end=644,
)

DESCRIPTOR.message_types_by_name['file'] = _FILE
DESCRIPTOR.message_types_by_name['getdata_request'] = _GETDATA_REQUEST
DESCRIPTOR.message_types_by_name['delegate_file'] = _DELEGATE_FILE
DESCRIPTOR.message_types_by_name['delegate_erasure_file'] = _DELEGATE_ERASURE_FILE
DESCRIPTOR.message_types_by_name['delegate_get_erasure_file'] = _DELEGATE_GET_ERASURE_FILE
DESCRIPTOR.message_types_by_name['broadcast_request_file'] = _BROADCAST_REQUEST_FILE
DESCRIPTOR.message_types_by_name['broadcast_response_node'] = _BROADCAST_RESPONSE_NODE
DESCRIPTOR.message_types_by_name['broadcast_request_specefic'] = _BROADCAST_REQUEST_SPECEFIC
DESCRIPTOR.message_types_by_name['broadcast_request_fragment'] = _BROADCAST_REQUEST_FRAGMENT
DESCRIPTOR.message_types_by_name['worker_store_file_response'] = _WORKER_STORE_FILE_RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

file = _reflection.GeneratedProtocolMessageType('file', (_message.Message,), {
  'DESCRIPTOR' : _FILE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:file)
  })
_sym_db.RegisterMessage(file)

getdata_request = _reflection.GeneratedProtocolMessageType('getdata_request', (_message.Message,), {
  'DESCRIPTOR' : _GETDATA_REQUEST,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:getdata_request)
  })
_sym_db.RegisterMessage(getdata_request)

delegate_file = _reflection.GeneratedProtocolMessageType('delegate_file', (_message.Message,), {
  'DESCRIPTOR' : _DELEGATE_FILE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:delegate_file)
  })
_sym_db.RegisterMessage(delegate_file)

delegate_erasure_file = _reflection.GeneratedProtocolMessageType('delegate_erasure_file', (_message.Message,), {
  'DESCRIPTOR' : _DELEGATE_ERASURE_FILE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:delegate_erasure_file)
  })
_sym_db.RegisterMessage(delegate_erasure_file)

delegate_get_erasure_file = _reflection.GeneratedProtocolMessageType('delegate_get_erasure_file', (_message.Message,), {
  'DESCRIPTOR' : _DELEGATE_GET_ERASURE_FILE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:delegate_get_erasure_file)
  })
_sym_db.RegisterMessage(delegate_get_erasure_file)

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

broadcast_request_fragment = _reflection.GeneratedProtocolMessageType('broadcast_request_fragment', (_message.Message,), {
  'DESCRIPTOR' : _BROADCAST_REQUEST_FRAGMENT,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:broadcast_request_fragment)
  })
_sym_db.RegisterMessage(broadcast_request_fragment)

worker_store_file_response = _reflection.GeneratedProtocolMessageType('worker_store_file_response', (_message.Message,), {
  'DESCRIPTOR' : _WORKER_STORE_FILE_RESPONSE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:worker_store_file_response)
  })
_sym_db.RegisterMessage(worker_store_file_response)


# @@protoc_insertion_point(module_scope)
