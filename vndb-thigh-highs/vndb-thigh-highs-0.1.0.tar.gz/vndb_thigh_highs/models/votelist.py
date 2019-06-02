from .flag import Flag
from .table import Table
from .types import INTEGER, TIMESTAMP

none = Flag.NONE
basic = Flag.BASIC

class Votelist(Table):
    user_id = none.Column(INTEGER).with_name('uid')
    vn_id = basic.Column(INTEGER).with_name('vn')
    vote = basic.Column(INTEGER)
    added = basic.Column(TIMESTAMP)
