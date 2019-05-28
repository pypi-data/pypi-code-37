__all__ = ['api']

from quaerere_base_client.api import API

from .resources import (WebSiteResource, WebPageResource)

api = API('v1')
api.add_resource(WebPageResource)
api.add_resource(WebSiteResource)
