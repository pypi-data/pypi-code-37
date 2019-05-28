__all__ = ['WebPageResource']

from quaerere_base_client.resource import Resource
from willamette_common.schemas import WebPageSchema


class WebPageResource(Resource):
    resource_schema = WebPageSchema
    model_class = None
