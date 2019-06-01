import hmac
import json
import blihtz
import requests
from hashlib import sha512
from urllib.parse import urljoin, quote
from blihtz.exceptions import BlihtzException, NotFoundException, UnavailableException, AuthenticationException


class Blihtz:
    """The class used to interact with the API."""

    ENDPOINT = 'https://blih.epitech.eu'
    HEADERS = {
        'User-Agent': 'blihtz-' + str(blihtz.__version__),
        'Content-Type': 'application/json'
    }

    def __init__(self, username: str = None, password: str = None, token: str = None):
        """The class constructor."""

        self._keys = []
        self._repositories = []
        self.username = username
        self.token = None
        self.session = requests.Session()

        if password is not None:
            self.token = sha512(password.encode('utf-8')).hexdigest().encode('utf-8')
        if token is not None:
            self.token = token.encode('utf-8')

    @property
    def repositories(self):
        """Get all the repositories."""

        if self._repositories:
            return self._repositories

        data = self.request('repositories').json()
        repositories = data['repositories']

        for name in repositories:
            repository = blihtz.Repository(self, name, **repositories[name], fetch=False)

            self._repositories.append(repository)

        return self._repositories

    @property
    def keys(self):

        if self._keys:
            return self._keys

        keys = self.request('sshkeys').json()

        for name in keys:
            key = blihtz.Key(self, name, data=keys[name], fetch=False)

            self._keys.append(key)

        return self._keys

    def repository(self, name: str, **kwargs):
        """Repository helper."""

        return blihtz.Repository(self, name, **kwargs)

    def key(self, name: str, **kwargs):
        """Key helper."""

        return blihtz.Key(self, name, **kwargs)

    def sign(self, data=None):
        """Sign the given piece of data."""

        signature = hmac.new(self.token, msg=self.username.encode('utf-8'), digestmod=sha512)
        signed_data = {
            'user': self.username
        }

        if data is not None:
            signed_data['data'] = data
            payload = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

            signature.update(payload.encode('utf-8'))

        signed_data['signature'] = signature.hexdigest()

        return signed_data

    def request(self, path: str, method: str = 'GET', data=None):
        """Send a request."""

        if isinstance(path, list):
            path = '/'.join(path)

        url = urljoin(self.ENDPOINT, quote(path))

        try:
            r = self.session.request(method, url, json=self.sign(data), headers=self.HEADERS)

            r.raise_for_status()
        except (requests.ConnectionError, requests.Timeout) as exception:
            raise UnavailableException from exception
        except requests.RequestException as exception:
            if exception.response is None:
                raise BlihtzException from exception
            if exception.response.status_code == 401:
                raise AuthenticationException from exception
            if exception.response.status_code == 404:
                raise NotFoundException from exception

            raise BlihtzException from exception

        return r
