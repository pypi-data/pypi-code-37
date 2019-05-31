from watchdog.observers import Observer
from .XMMiniAppEventHandler import XMMiniAppEventHandler 
import sys
import time

class FileWatcher:
    def __init__(self, src_root):
        self.__src_root = src_root
        self.__event_handler = XMMiniAppEventHandler()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        # try:
        #     while True:
        #         time.sleep(1)
        # except KeyboardInterrupt:
        #     self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_root,
            recursive=True
        )