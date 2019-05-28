__all__ = ['WillametteClient']

from quaerere_base_client.client import Client

from .api_v1 import api as api_v1


class WillametteClient(Client):
    def __init__(self, url):
        super().__init__(url)
        self.add_api(api_v1)
