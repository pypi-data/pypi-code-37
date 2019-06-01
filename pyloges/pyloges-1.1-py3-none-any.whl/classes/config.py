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

import json

from pyloges.classes.interfaces.handler import Handler
from pyloges.handlers.std import StdHandler
from pyloges.handlers.file import FileHandler


class Config:
    """
    Logger configuration class.

    Pass it as an argument to logger __init__ method
    """
    log_level = 1
    log_message_format = "[{level}]{%y-%M-%d %h:%m:%s} - {msg}"
    exit_on_fatal = False
    _log_handlers = []

    def __init__(self, log_level=1, log_message_format="[{level}]{%y-%M-%d %h:%m:%s} - {msg}", print_to_std=True,
                 exit_on_fatal=False):
        self.log_level = log_level
        self.log_message_format = log_message_format
        self.exit_on_fatal = exit_on_fatal

        if print_to_std:
            self.add_handler(StdHandler())

    @classmethod
    def get_instance_from_file(cls, filename: str):
        """Loads config from json file"""
        file = open(filename, 'r')
        conf = json.loads(file.read())
        return Config(**conf)

    def add_writing_to_file(self, filename: str):
        """Adds handler that prints to file. You can use filename formatting"""
        self.add_handler(FileHandler(filename))

    def add_handler(self, handler: Handler):
        self._log_handlers += [handler]

    def get_handlers(self):
        return self._log_handlers
