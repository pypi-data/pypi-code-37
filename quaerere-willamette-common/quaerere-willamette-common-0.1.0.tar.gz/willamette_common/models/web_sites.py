__all__ = ['WebSiteBase']

from marshmallow import fields


class WebSiteBase:
    url = fields.Url(required=True)
    inLanguage = fields.String()
