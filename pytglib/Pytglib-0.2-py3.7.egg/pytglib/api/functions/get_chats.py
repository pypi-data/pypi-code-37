

from ..utils import Object


class GetChats(Object):
    """
    Returns an ordered list of chats. Chats are sorted by the pair (order, chat_id) in decreasing order. (For example, to get a list of chats from the beginning, the offset_order should be equal to a biggest signed 64-bit number 9223372036854775807 == 2^63 - 1).For optimal performance the number of returned chats is chosen by the library. 

    Attributes:
        ID (:obj:`str`): ``GetChats``

    Args:
        offset_order (:obj:`int`):
            Chat order to return chats from 
        offset_chat_id (:obj:`int`):
            Chat identifier to return chats from
        limit (:obj:`int`):
            The maximum number of chats to be returnedIt is possible that fewer chats than the limit are returned even if the end of the list is not reached

    Returns:
        Chats

    Raises:
        :class:`telegram.Error`
    """
    ID = "getChats"

    def __init__(self, offset_order, offset_chat_id, limit, extra=None, **kwargs):
        self.extra = extra
        self.offset_order = offset_order  # int
        self.offset_chat_id = offset_chat_id  # int
        self.limit = limit  # int

    @staticmethod
    def read(q: dict, *args) -> "GetChats":
        offset_order = q.get('offset_order')
        offset_chat_id = q.get('offset_chat_id')
        limit = q.get('limit')
        return GetChats(offset_order, offset_chat_id, limit)
