import requests
import socket
import datetime
from cuculus import CuculusClient


class CuculusLogger:

    def __init__(self,
                 cuculusClient: CuculusClient,
                 name,
                 appId,
                 hostname=socket.gethostname(),
                 logger=None
                 ):
        self.cuculusClient = cuculusClient
        self.name = name
        self.appId = appId
        self.hostname = hostname
        self.logger = logger

    def info(self, message):
        self.log(message, 2)

    def warn(self, message):
        self.log(message, 3)

    def error(self, message):
        self.log(message, 4)

    def log(self, message, level=2):
        try:
            data = {
                "AppId": self.appId,
                "Message": message,
                "Logger": self.name,
                "Host": self.hostname,
                "Level": level,
                "Timestamp": datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
            }
            self.cuculusClient.addLog(data)
        except Exception as e:
            if(self.logger != None):
                self.logger.error(e)
