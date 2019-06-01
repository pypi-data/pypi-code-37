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

import datetime

from pyloges.classes.interfaces.handler import Handler


class FileHandler(Handler):
    """Handler that saves logs to file"""
    filename = ""
    log = ""

    def __init__(self, filename: str):
        self.filename = _process_filename(filename)

    def print_log(self, msg: str):
        self.log += msg + "\n"

    def save(self):
        f = open(self.filename, "w")
        f.write(self.log)
        f.close()


def _process_filename(filename: str) -> str:
    tt = datetime.datetime.now().timetuple()

    new_str = filename
    new_str = new_str.replace("%y", str(tt.tm_year))
    new_str = new_str.replace("%M", str(tt.tm_mon) if tt.tm_mon >= 10 else "0" + str(tt.tm_mon))
    new_str = new_str.replace("%d", str(tt.tm_mday) if tt.tm_mday >= 10 else "0" + str(tt.tm_mday))
    new_str = new_str.replace("%h", str(tt.tm_hour))
    new_str = new_str.replace("%m", str(tt.tm_min) if tt.tm_min >= 10 else "0" + str(tt.tm_min))
    new_str = new_str.replace("%s", str(tt.tm_sec) if tt.tm_sec >= 10 else "0" + str(tt.tm_sec))

    return new_str
