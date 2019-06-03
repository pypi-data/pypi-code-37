import requests
import socket
import datetime
import multiprocessing
import threading
from time import ctime, sleep
from cuculus import CuculusClientOptions


class CuculusClient:

    def __init__(self,
                 collectorUrl,
                 options: CuculusClientOptions,
                 logger=None):
        '''
        :param appId:string Application Id
        :param collectorUrl:string url of collector service. eg: http://139.217.138.15:6280/api/v1/Log
        :param logger use to print CuculusClient self produced log.
        :return: int
        '''

        self.collectorUrl = collectorUrl
        self.logger = logger
        self.maxQueueSize = options.maxQueueSize
        self.cleanSizeWhenFull = options.cleanSizeWhenFull
        self.sendBatchSize = options.sendBatchSize
        self.sendTryTimes = options.sendTryTimes

        self.queue = multiprocessing.Queue(options.maxQueueSize)
        self.isCanncelQueue = multiprocessing.Queue(1)
        self.isCanncelQueue.put(0)

    def addLog(self, log):
        if(self.queue.full()):
            for target_list in range(self.cleanSizeWhenFull):
                if self.queue.empty():
                    break
                self.queue.get(False, 0)
        try:
            self.queue.put_nowait(log)
        except Exception as ex:
            print(ex)

    def start(self):
        self.thread = threading.Thread(target=self.__run, args=(self,))
        self.thread.setDaemon(True)
        self.thread.setName("Cuculus Client Thread")
        self.thread.start()

    def __run(self, fun):
        while not self.isCanncelQueue.empty():
            sendNextBatch = True
            while sendNextBatch:
                if self.queue.empty():
                    break
                else:
                    try:
                        if self.queue.qsize() > self.sendBatchSize:
                            batchSize = self.sendBatchSize
                        else:
                            batchSize = self.queue.qsize()
                            sendNextBatch = False
                        logs = []
                        for target_list in range(batchSize):
                            logs.append(self.queue.get_nowait())

                        self.__logInfo(logs)
                    except Exception as ex:
                        pass
            sleep(3)
        # print("run end")

    def stop(self):
        if(self.isCanncelQueue.qsize() > 0):
            obj = self.isCanncelQueue.get(False)
            # print(obj)

    def __logInfo(self, logs):
        for target_list in range(self.sendTryTimes):
            try:
                data = logs
                requests.post(
                    self.collectorUrl,
                    headers={'Content-Type': 'application/json'},
                    json=data)
                break
            except Exception as e:
                if(self.logger != None):
                    self.logger.error(e)
                if(self.queue.full()):
                    break
