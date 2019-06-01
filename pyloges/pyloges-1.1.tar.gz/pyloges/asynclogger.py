# Copyright (C) 2018 Nikita S., Koni Dev Team, All Rights Reserved
# https://github.com/Nekit10/pyloges
#
# This file is part of Pyloges.
#
# Pyloges is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyloges is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyloges.  If not, see <https://www.gnu.org/licenses/>.

from threading import Thread
from queue import Queue

from pyloges.classes.config import Config
from pyloges.logger import Logger


class AsyncLogger(Logger):
    """Logger that saves logs in another thread"""

    def __init__(self, config: Config):
        super().__init__(config)
        self.queue = Queue()
        self.thread = AsyncLoggerThread(self.queue, self)
        self.thread.start()

    def log_async(self, msg: str, log_level: int, log_level_config: int):
        """Thread will call this method to save log"""
        super().log(msg, log_level, log_level_config)

    def log(self, msg: str, log_level: int, log_level_config=-1):
        """Passes log to thread"""
        self.queue.put({"msg": msg, "level": log_level,
                        "level_config": self.config.log_level if log_level_config == -1 else log_level_config})

    def wait(self):
        self.queue.join()
        self.thread.stop()


class AsyncLoggerThread(Thread):

    is_stopping = False

    def __init__(self, queue: Queue, log_class: AsyncLogger):
        Thread.__init__(self)
        self.queue = queue
        self.log_class = log_class

    def stop(self):
        self.is_stopping = True

    def run(self) -> None:
        while True:
            if self.is_stopping:
                break
            log = self.queue.get()
            self.log_class.log_async(log["msg"], log["level"], log["level_config"])
            self.queue.task_done()
