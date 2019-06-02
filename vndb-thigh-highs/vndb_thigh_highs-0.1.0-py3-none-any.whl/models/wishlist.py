from enum import Enum
from .flag import Flag
from .table import Table
from .types import INTEGER, TIMESTAMP

class Priority(Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2
    BLACKLIST = 3

none = Flag.NONE
basic = Flag.BASIC

class Wishlist(Table):
    user_id = none.Column(INTEGER).with_name('uid')
    vn_id = basic.Column(INTEGER).with_name('vn')
    priority = basic.Column(Priority)
    added = basic.Column(TIMESTAMP)
