# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from epl.protobuf import geometry_pb2 as epl_dot_protobuf_dot_geometry__pb2


class GeometryServiceStub(object):
  """
  gRPC Interfaces for working with geometry operators
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GeometryOperationUnary = channel.unary_unary(
        '/epl.grpc.GeometryService/GeometryOperationUnary',
        request_serializer=epl_dot_protobuf_dot_geometry__pb2.GeometryRequest.SerializeToString,
        response_deserializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.FromString,
        )
    self.GeometryOperationBiStream = channel.stream_stream(
        '/epl.grpc.GeometryService/GeometryOperationBiStream',
        request_serializer=epl_dot_protobuf_dot_geometry__pb2.GeometryRequest.SerializeToString,
        response_deserializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.FromString,
        )
    self.GeometryOperationBiStreamFlow = channel.stream_stream(
        '/epl.grpc.GeometryService/GeometryOperationBiStreamFlow',
        request_serializer=epl_dot_protobuf_dot_geometry__pb2.GeometryRequest.SerializeToString,
        response_deserializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.FromString,
        )
    self.FileOperationBiStreamFlow = channel.stream_stream(
        '/epl.grpc.GeometryService/FileOperationBiStreamFlow',
        request_serializer=epl_dot_protobuf_dot_geometry__pb2.FileRequestChunk.SerializeToString,
        response_deserializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.FromString,
        )


class GeometryServiceServicer(object):
  """
  gRPC Interfaces for working with geometry operators
  """

  def GeometryOperationUnary(self, request, context):
    """Execute a single blocking geometry operation
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GeometryOperationBiStream(self, request_iterator, context):
    """stream in operator requests and get back a stream of results
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GeometryOperationBiStreamFlow(self, request_iterator, context):
    """manual flow control bi-directional stream. example
    go shouldn't use this because of https://groups.google.com/forum/#!topic/grpc-io/6_B46Oszb4k ?
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def FileOperationBiStreamFlow(self, request_iterator, context):
    """Maybe a cut operation that returns a lot of different geometries? for now, this is not implemented.
    rpc GeometryOperationServerStream(epl.protobuf.GeometryRequest) returns (stream epl.protobuf.GeometryResponse) {}

    Maybe something like a union operation. for now, this is not implemented.
    rpc GeometryOperationClientStream(stream epl.protobuf.GeometryRequest) returns (epl.protobuf.GeometryResponse) {}

    stream in file chunks for a geometry file type and stream back results for each geometry encountered
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GeometryServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GeometryOperationUnary': grpc.unary_unary_rpc_method_handler(
          servicer.GeometryOperationUnary,
          request_deserializer=epl_dot_protobuf_dot_geometry__pb2.GeometryRequest.FromString,
          response_serializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.SerializeToString,
      ),
      'GeometryOperationBiStream': grpc.stream_stream_rpc_method_handler(
          servicer.GeometryOperationBiStream,
          request_deserializer=epl_dot_protobuf_dot_geometry__pb2.GeometryRequest.FromString,
          response_serializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.SerializeToString,
      ),
      'GeometryOperationBiStreamFlow': grpc.stream_stream_rpc_method_handler(
          servicer.GeometryOperationBiStreamFlow,
          request_deserializer=epl_dot_protobuf_dot_geometry__pb2.GeometryRequest.FromString,
          response_serializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.SerializeToString,
      ),
      'FileOperationBiStreamFlow': grpc.stream_stream_rpc_method_handler(
          servicer.FileOperationBiStreamFlow,
          request_deserializer=epl_dot_protobuf_dot_geometry__pb2.FileRequestChunk.FromString,
          response_serializer=epl_dot_protobuf_dot_geometry__pb2.GeometryResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'epl.grpc.GeometryService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
