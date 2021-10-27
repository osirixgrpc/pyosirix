# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: browsercontroller.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import osirix.pb2.utilities_pb2 as utilities__pb2
import osirix.pb2.types_pb2 as types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='browsercontroller.proto',
  package='osirixgrpc',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x62rowsercontroller.proto\x12\nosirixgrpc\x1a\x0futilities.proto\x1a\x0btypes.proto\"\xa2\x01\n*BrowserControllerDatabaseSelectionResponse\x12\"\n\x06status\x18\x01 \x01(\x0b\x32\x12.osirixgrpc.Status\x12\'\n\x06series\x18\x02 \x03(\x0b\x32\x17.osirixgrpc.DicomSeries\x12\'\n\x07studies\x18\x03 \x03(\x0b\x32\x16.osirixgrpc.DicomStudy\"j\n)BrowserControllerCopyFilesIfNeededRequest\x12.\n\x07\x62rowser\x18\x01 \x01(\x0b\x32\x1d.osirixgrpc.BrowserController\x12\r\n\x05paths\x18\x02 \x03(\tb\x06proto3'
  ,
  dependencies=[utilities__pb2.DESCRIPTOR,types__pb2.DESCRIPTOR,])




_BROWSERCONTROLLERDATABASESELECTIONRESPONSE = _descriptor.Descriptor(
  name='BrowserControllerDatabaseSelectionResponse',
  full_name='osirixgrpc.BrowserControllerDatabaseSelectionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='osirixgrpc.BrowserControllerDatabaseSelectionResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='series', full_name='osirixgrpc.BrowserControllerDatabaseSelectionResponse.series', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='studies', full_name='osirixgrpc.BrowserControllerDatabaseSelectionResponse.studies', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=70,
  serialized_end=232,
)


_BROWSERCONTROLLERCOPYFILESIFNEEDEDREQUEST = _descriptor.Descriptor(
  name='BrowserControllerCopyFilesIfNeededRequest',
  full_name='osirixgrpc.BrowserControllerCopyFilesIfNeededRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='browser', full_name='osirixgrpc.BrowserControllerCopyFilesIfNeededRequest.browser', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='paths', full_name='osirixgrpc.BrowserControllerCopyFilesIfNeededRequest.paths', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=234,
  serialized_end=340,
)

_BROWSERCONTROLLERDATABASESELECTIONRESPONSE.fields_by_name['status'].message_type = utilities__pb2._STATUS
_BROWSERCONTROLLERDATABASESELECTIONRESPONSE.fields_by_name['series'].message_type = types__pb2._DICOMSERIES
_BROWSERCONTROLLERDATABASESELECTIONRESPONSE.fields_by_name['studies'].message_type = types__pb2._DICOMSTUDY
_BROWSERCONTROLLERCOPYFILESIFNEEDEDREQUEST.fields_by_name['browser'].message_type = types__pb2._BROWSERCONTROLLER
DESCRIPTOR.message_types_by_name['BrowserControllerDatabaseSelectionResponse'] = _BROWSERCONTROLLERDATABASESELECTIONRESPONSE
DESCRIPTOR.message_types_by_name['BrowserControllerCopyFilesIfNeededRequest'] = _BROWSERCONTROLLERCOPYFILESIFNEEDEDREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BrowserControllerDatabaseSelectionResponse = _reflection.GeneratedProtocolMessageType('BrowserControllerDatabaseSelectionResponse', (_message.Message,), {
  'DESCRIPTOR' : _BROWSERCONTROLLERDATABASESELECTIONRESPONSE,
  '__module__' : 'browsercontroller_pb2'
  # @@protoc_insertion_point(class_scope:osirixgrpc.BrowserControllerDatabaseSelectionResponse)
  })
_sym_db.RegisterMessage(BrowserControllerDatabaseSelectionResponse)

BrowserControllerCopyFilesIfNeededRequest = _reflection.GeneratedProtocolMessageType('BrowserControllerCopyFilesIfNeededRequest', (_message.Message,), {
  'DESCRIPTOR' : _BROWSERCONTROLLERCOPYFILESIFNEEDEDREQUEST,
  '__module__' : 'browsercontroller_pb2'
  # @@protoc_insertion_point(class_scope:osirixgrpc.BrowserControllerCopyFilesIfNeededRequest)
  })
_sym_db.RegisterMessage(BrowserControllerCopyFilesIfNeededRequest)


# @@protoc_insertion_point(module_scope)
