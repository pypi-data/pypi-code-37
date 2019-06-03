import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class Serializer:
    def serialize(self, request, bundle):
        raise NotImplementedError()

    def clean_item(self, item, project):
        to_drop = [
            k
            for k in item.keys()
            if k not in project
        ]

        for k in to_drop:
            del item[k]

    def apply_project(self, bundle):
        project = bundle.get("project")

        if project:
            for item in bundle["items"]:
                self.clean_item(item, project)

    def get_data(self, bundle):
        _data = {}

        self.apply_project(bundle)

        _items = bundle.get("items", [])

        if len(_items) is 1:
            _data["item"] = _items[0]
        else:
            _data["items"] = _items

        for item in [
            'filter',
            'order',
            'project',
            'error_code',
            'error_message',
            'status_code',
            'limit',
            'skip',
            'total',
            'created',
            'updated',
            'deleted',
        ]:
            if bundle.get(item) is not None:
                _data[item] = bundle[item]

        return _data


class DjangoSerializer(Serializer):
    @staticmethod
    def get_encoder():
        return DjangoJSONEncoder

    def serialize(self, request, bundle):
        _data = self.get_data(bundle)

        return JsonResponse(_data, status=bundle['status_code'], encoder=self.get_encoder())


class JSONSerializer(Serializer):
    @staticmethod
    def get_encoder():
        return json.JSONEncoder

    def serialize(self, request, bundle):
        _data = self.get_data(bundle)

        return json.dumps(_data, cls=self.get_encoder())
