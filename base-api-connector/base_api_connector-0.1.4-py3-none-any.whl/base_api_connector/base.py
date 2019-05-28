import requests
import inspect


POSSIBLE_COMMANDS = ('list', 'create', 'retrieve', 'update', 'destroy')


# TODO: not sure if I like this concept...
class CommandMethodHolder:  # TODO: upgrade Response object r with helpful stuff like accessing the id when using create
    def get_full_url(self, pk=None):
        raise NotImplementedError

    def list(self):  # TODO: also, do I want validation for data?
        def list(**kwargs):
            url = self.get_full_url()
            r = requests.get(url, **kwargs)
            return r
        return list

    def create(self):
        def create(data, **kwargs):
            if isinstance(data, AsDictObject):
                data = data.as_dict()
            url = self.get_full_url()
            r = requests.post(url, data, **kwargs)
            return r
        return create

    def retrieve(self):
        def retrieve(pk, **kwargs):
            url = self.get_full_url(pk)
            r = requests.get(url, **kwargs)
            return r
        return retrieve

    def update(self):
        def update(pk, data, **kwargs):
            if isinstance(data, AsDictObject):
                data = data.as_dict()
            url = self.get_full_url(pk)
            r = requests.patch(url, data, **kwargs)
            return r
        return update

    def destroy(self):
        def destroy(pk, **kwargs):
            url = self.get_full_url(pk)
            r = requests.delete(url, **kwargs)
            return r
        return destroy


class APIResource:
    api = type('EmptyAPIConnector', (), {'base_api_url': '/'})
    name = ''

    def list(self, **kwargs):
        raise NotImplementedError

    def create(self, data, **kwargs):
        raise NotImplementedError

    def retrieve(self, pk, **kwargs):
        raise NotImplementedError

    def update(self, pk, data, **kwargs):
        raise NotImplementedError

    def destroy(self, pk, **kwargs):
        raise NotImplementedError

    def __init__(self, commands, *args, **kwargs):
        if commands == 'all':
            commands = POSSIBLE_COMMANDS
        for command in commands:
            setattr(self, command, getattr(CommandMethodHolder, command)(self))

    def get_full_url(self, pk=''):
        return f'{self.api.base_api_url}{self.name}/{pk}'


class GenericAPIConnector:
    def __new__(cls):
        for name in dir(cls):
            attr = getattr(cls, name)
            if isinstance(attr, APIResource):
                attr.api = cls
                attr.name = name
        return object.__new__(cls)

    base_data = {}  # add base data
    base_headers = {}  # add base headers
    resource_config = None

    @property
    def base_api_url(self):
        raise NotImplementedError


class AsDictObject:
    def as_dict(self):
        attributes = inspect.getmembers(self, lambda a: not inspect.isroutine(a))
        dict_repr = {}
        for name, value in attributes:
            if '_' not in name[0]:
                if isinstance(value, AsDictObject):
                    value = value.as_dict()
                elif isinstance(value, list):
                    value = [i.as_dict() if isinstance(i, AsDictObject) else i for i in value]

                if callable(value):
                    dict_repr[name] = value()
                else:
                    dict_repr[name] = value
        return dict_repr


# TODO: make a program that can go through django and generate code for a connector taht you can copy paste into where you use it
