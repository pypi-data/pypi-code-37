import os
from urllib.parse import urljoin

import requests

ENDPOINT = 'https://api.isl.co/v1/'


class ISLException(Exception):
    pass


class ResourceList:

    def __init__(self, client, resource):
        self.client = client
        self.resource = resource
        self.params = {}

    def __iter__(self):
        data = self.client._call('GET', self.resource, self.params)
        for record in data:
            yield record

    def get(self, id_):
        res = ResourceDetail(self.client, self.resource, id_)
        res.params.update(self.params)
        return res.get()

    def list(self):
        return list(self)

    def fields(self, *args):
        self.params['fields'] = ','.join(args)
        return self

    def limit(self, val):
        self.params['limit'] = val
        return self

    def page(self, val):
        self.params['page'] = val
        return self


class ResourceDetail:

    def __init__(self, client, resource, id_):
        self.client = client
        self.path = '{}/{}'.format(resource, id_)
        self.params = {}

    def get(self):
        return self.client._call('GET', self.path, self.params)

    def fields(self, *args):
        self.params['fields'] = ','.join(args)
        return self


class ISLClient:

    def __init__(self, key, endpoint=None):
        self.endpoint = endpoint or ENDPOINT
        session = requests.Session()
        session.headers = {
            'Authorization': 'Token {}'.format(key),
        }
        session.headers.update({
            'User-Agent':
                'python-isl (+https://github.com/istrategylabs/python-isl)',
        })
        self._session = session

    def _call(self, method, path='', params=None):

        if not self._session:
            raise Exception('auth required')

        url = urljoin(self.endpoint, path)
        if not url.endswith('/'):
            url += '/'

        if method == 'GET':
            resp = self._session.get(url, params=params)
        elif method == 'POST':
            resp = None
        else:
            raise ValueError('invalid method')

        if resp.status_code == 200:
            return resp.json()

    def employee(self, username):
        return ResourceDetail(self, 'employees', username)

    def employees(self):
        return ResourceList(self, 'employees')

    def dog(self, name):
        return ResourceDetail(self, 'dogs', name)

    def dogs(self):
        return ResourceList(self, 'dogs')

    def team(self, name):
        return ResourceDetail(self, 'teams', name)

    def teams(self):
        return ResourceList(self, 'teams')

    def test(self):
        try:
            self._call('GET', 'health')
            return True
        except:
            pass

if __name__ == '__main__':

    access_token = os.environ.get('ISL_ACCESS_TOKEN')

    isl = ISLClient(access_token)

    if not isl.test():
        raise ISLException('whoa')

    print(isl.teams().list())
    print(isl.employees().list())
    print(isl.teams().fields('members').get('antimatter'))
    print(isl.team('antimatter').fields('name').get())

    for dog in isl.dogs():
        print(dog)

    print(isl.dogs().fields('slug', 'photo').get('gojo'))
