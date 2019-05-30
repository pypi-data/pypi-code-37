import grpc
from . import xurpc_pb2 as xu
from .xurpc_pb2_grpc import XudStub
import logging


class Xud:
    def __init__(self, connstr, cert):
        creds = grpc.ssl_channel_credentials(cert)
        channel = grpc.secure_channel(connstr, creds)
        self.client = XudStub(channel)

    @property
    def status(self):
        try:
            print(self.client.GetInfo(xu.GetInfoRequest()))
            return "Running"
        except:
            logging.exception('Xud failed to get status')
            return "Error"
