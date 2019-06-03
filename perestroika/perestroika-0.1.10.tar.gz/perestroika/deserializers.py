import json
from json import JSONDecodeError

from perestroika.exceptions import BadRequest
from perestroika.utils import multi_dict_to_dict


class Deserializer:
    def get_data(self, request, method_handler, **kwargs):
        raise NotImplementedError()

    def deserialize(self, request, method_handler, **kwargs):
        _data = self.get_data(request, method_handler, **kwargs)

        _items = _data.get("items", [])
        _item = _data.get("item")

        if _item:
            _items = [_item]

        if not _items and request.method.lower() in ["post", "put", "patch"]:
            raise BadRequest(message="Need data for processing")

        bundle = {
            "order": _data.get("order", {}),
            "filter": _data.get("filter", {}),
            "items": _items,
            "queryset": method_handler.queryset,
            "project": _data.get("project", []),
            "meta": _data.get("meta", {}),
        }

        return bundle


class DjangoDeserializer(Deserializer):
    def get_data(self, request, method_handler, **kwargs):
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            data = {}

        if request.method == 'GET':
            uri_data = multi_dict_to_dict(request.GET)
            data.update(uri_data)

        return data


class JSONDeserializer(Deserializer):
    def get_data(self, request, method_handler, **kwargs):
        return kwargs.get("json_data", {})
