__all__ = ['WebPageBase']

from marshmallow import fields


class WebPageBase:
    text = fields.String()
    url = fields.Url(required=True)
    web_site_key = fields.String()
