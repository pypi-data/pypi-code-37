import socket
from cuculus import CuculusClient
from cuculus import CuculusLogger
from cuculus import CuculusClientOptions


class CuculusLoggerFactory:
    def __init__(self, appId, collectorUrl,
                 options: CuculusClientOptions = CuculusClientOptions(),
                 logger=None,
                 hostname=socket.gethostname()):

        self.appId = appId
        self.logger = logger
        self.hostname = hostname
        self.client = CuculusClient(
            collectorUrl, options, logger)
        self.client.start()

    def createLogger(self, name):
        return CuculusLogger(self.client, name, self.appId, self.hostname, self.logger)
