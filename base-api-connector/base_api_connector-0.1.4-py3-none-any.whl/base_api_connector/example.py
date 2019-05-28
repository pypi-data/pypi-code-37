from .base import GenericAPIConnector, AsDictObject, CommandMethodHolder, APIResource


class UserObject(AsDictObject):
    name = 'test'


class ImplementedAPIConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    users = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))
    postboxes = APIResource(('retrieve',))
    notes = APIResource('all')
    tags = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))
    types = APIResource(('create', 'retrieve', 'update', 'destroy', 'list'))


conn = ImplementedAPIConnector()
# print(conn.notes.list())
print(dir(CommandMethodHolder))
conn.users.list()
if __name__ == "__main__":
    pass
