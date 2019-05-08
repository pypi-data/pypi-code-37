

from ..utils import Object


class UserStatus(Object):
    """
    Describes the last time the user was online

    No parameters required.
    """
    ID = "userStatus"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "UserStatusOffline or UserStatusOnline or UserStatusRecently or UserStatusLastWeek or UserStatusEmpty or UserStatusLastMonth":
        if q.get("@type"):
            return Object.read(q)
        return UserStatus()
