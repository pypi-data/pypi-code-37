import socket


class CuculusClientOptions:
    def __init__(self):
        self.maxQueueSize = 100000
        self.cleanSizeWhenFull = 100
        self.sendBatchSize = 1000
        self.sendTryTimes = 3
        #self.hostname = socket.gethostname()
        #return super().__init__()
