from perestroika.exceptions import BadRequest


class DbLayer:
    pass


class DjangoDbLayer(DbLayer):
    @staticmethod
    def get(bundle, method):
        _filter = bundle.get("filter")
        _exclude = bundle.get("exclude")
        _project = bundle.get("project")

        if _filter:
            bundle["queryset"] = bundle["queryset"].filter(_filter)

        if _exclude:
            bundle["queryset"] = bundle["queryset"].exclude(_exclude)

        if _project:
            bundle["queryset"] = bundle["queryset"].only(*_project)

        bundle["items"] = bundle["queryset"].values()

        if method.count_total:
            bundle["total"] = bundle["queryset"].count()

    @staticmethod
    def post(bundle, method):
        items = bundle.get("items")

        if not items:
            raise BadRequest(message="Empty data for resource")

        items = [bundle["queryset"].model(**data) for data in items]

        bundle["queryset"].model.objects.bulk_create(items)
        bundle["created"] = len(items)

        if method.count_total:
            bundle["total"] = bundle["queryset"].count()

    @staticmethod
    def put(bundle, method):
        items = bundle.get("items")

        if not items:
            raise BadRequest(message="Empty data for resource")

        updated = 0

        for item in items:
            updated += bundle["queryset"].update(**item)

        bundle["updated"] = updated

        if method.count_total:
            bundle["total"] = bundle["queryset"].count()
