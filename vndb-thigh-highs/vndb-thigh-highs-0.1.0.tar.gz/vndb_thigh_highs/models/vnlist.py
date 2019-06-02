from enum import Enum
from .flag import Flag
from .table import Table
from .types import INTEGER, STRING, TIMESTAMP

class PlayingStatus(Enum):
    UNKNOW = 0
    PLAYING = 1
    FINISHED = 2
    STALLED = 3
    DROPPED = 4

none = Flag.NONE
basic = Flag.BASIC

class VNList(Table):
    user_id = none.Column(INTEGER).with_name('uid')
    vn_id = basic.Column(INTEGER).with_name('vn')
    status = basic.Column(PlayingStatus)
    added = basic.Column(TIMESTAMP)
    notes = basic.Column(STRING)
