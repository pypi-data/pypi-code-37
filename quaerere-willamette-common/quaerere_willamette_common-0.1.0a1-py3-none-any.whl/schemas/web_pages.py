__all__ = ['WebPageSchema']

from marshmallow import fields
from quaerere_base_common.schema import BaseSchema

from ..models import WebPageBase


class WebPageSchema(BaseSchema, WebPageBase):
    _key = fields.String()
