from .blihtz import Blihtz
from urllib.parse import quote
from .exceptions import NotFoundException


class Key:
    """The key class."""

    def __init__(self, blihtz: Blihtz, name: str, fetch: bool = False, **kwargs):
        """The class constructor."""

        self.name = name
        self.blihtz = blihtz
        self.deleted = False
        self._fetched = False
        self._data = kwargs.get('data', None)

        if fetch:
            self.fetch()

    def __str__(self):
        """The textual representation of this class."""

        return self.data

    @property
    def data(self):
        """The data property."""

        if not self._fetched:
            self.fetch()

        return self._data

    def fetch(self):
        """Fetch the key data."""

        data = self.blihtz.request('sshkeys').json()

        try:
            self._data = data[self.name]
        except KeyError as exception:
            raise NotFoundException from exception

        self._fetched = True

        return self

    def create(self):
        """Create the key."""

        self.blihtz.request('sshkeys', method='POST', data={
            'sshkey': quote(self._data.strip('\n'))
        })

        self.deleted = False

        return self

    def delete(self):
        """Delete the key."""

        self.blihtz.request(['sshkeys', self.name], method='DELETE')

        self.deleted = True

        return True
