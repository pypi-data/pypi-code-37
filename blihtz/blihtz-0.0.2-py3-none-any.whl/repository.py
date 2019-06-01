from .blihtz import Blihtz
from datetime import datetime


class Repository:
    """The repository model."""

    def __init__(self, blihtz: Blihtz, name: str, fetch: bool = False, **kwargs):
        """The class constructor."""

        self.name = name
        self.blihtz = blihtz
        self.deleted = False
        self._fetched = False
        self._url = kwargs.get('url', None)
        self._uuid = kwargs.get('uuid', None)
        self.type = kwargs.get('type', 'git')
        self.deleted = kwargs.get('deleted', False)
        self._public = kwargs.get('public', False)
        self._permissions = kwargs.get('permissions', [])
        self._created_at = kwargs.get('created_at', None)
        self._description = kwargs.get('description', None)

        if fetch:
            self.fetch()

    @property
    def uuid(self):
        """The UUID property."""

        if not self._fetched:
            self.fetch()

        return self._uuid

    @property
    def created_at(self):
        """The creation date property."""

        if not self._fetched:
            self.fetch()

        return self._created_at

    @created_at.setter
    def created_at(self, timestamp: int):
        """Set the creation time of the the repository."""

        self._created_at = datetime.fromtimestamp(timestamp)

    @property
    def public(self):
        """The public property."""

        if not self._fetched:
            self.fetch()

        return self._public

    @property
    def url(self):
        """The URL property."""

        if not self._fetched:
            self.fetch()

        return self._url

    @property
    def permissions(self):
        """Get permissions of the repository."""

        if self._permissions:
            return self._permissions

        data = self.blihtz.request(['repository', self.name, 'acls']).json()

        for user in data:
            self._permissions.append({'username': user, 'acl': data[user]})

        return self._permissions

    @permissions.setter
    def permissions(self, permissions: list):
        """Set the permissions of the repository."""

        for permission in permissions:
            if permission not in self.permissions:
                self.blihtz.request(['repository', self.name, 'acls'], method='POST', data={
                    'user': permission['username'], 'acl': permission['acl']
                })

        for permission in self._permissions:
            if permission not in permissions:
                self.blihtz.request(['repository', self.name, 'acls'], method='POST', data={
                    'user': permission['username'], 'acl': ''
                })

        self._permissions = []

    def create(self):
        """Create the repository."""

        self.blihtz.request('repositories', method='POST', data={
            'name': self.name,
            'type': self.type
        })

        self.deleted = False

        return self

    def fetch(self):
        """Fetch repository data."""

        data = self.blihtz.request(['repository', self.name]).json()

        self._url = str(data['message']['url'])
        self._uuid = str(data['message']['uuid'])
        self._public = bool(data['message']['public'])
        self._description = str(data['message']['description'])
        self.created_at = int(data['message']['creation_time'])
        self._fetched = True

        return self

    def delete(self):
        """Delete the repository."""

        self.blihtz.request(['repository', self.name], method='DELETE')

        self.deleted = True

        return True
