__all__ = ['WebSiteSchema']

from marshmallow import fields
from quaerere_base_common.schema import BaseSchema

from ..models import WebSiteBase


class WebSiteSchema(BaseSchema, WebSiteBase):
    _key = fields.String()
