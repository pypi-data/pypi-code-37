from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from import_export.admin import ImportMixin
from import_export.formats.base_formats import CSV

from .models import Vendor, Subject, Type
from .resources import VendorResource


class BlankFilter(admin.SimpleListFilter):
    """
    Filter a field by blank values (empty strings)
    http://stackoverflow.com/a/9593302/519510
    """
    title = ""
    parameter_name = ""

    def lookups(self, request, model_admin):
        return (
            ("1", "Yes"),
            ("0", "No"),
        )

    def queryset(self, request, queryset):
        kwargs = {
            unicode(self.parameter_name): "",
        }
        if self.value() == "0":
            return queryset.filter(**kwargs)
        if self.value() == "1":
            return queryset.exclude(**kwargs)
        return queryset


class GeolocationFilter(BlankFilter):
    """
    Filter by vendors that still need their geolocation set
    """
    title = "Added to map"
    parameter_name = "geolocation"


class CustomCSV(CSV):
    """
    CSV import format definition
    """

    def create_dataset(self, in_stream, **kwargs):
        """
        Copy of the original method of the CSV class.
        Fix an error created by the encode() call by commenting it out.
        """
        # if sys.version_info[0] < 3:
        #     # python 2.7 csv does not do unicode
        #     return super(CSV, self).create_dataset(in_stream.encode('utf-8'), **kwargs)
        return super(CSV, self).create_dataset(in_stream, **kwargs)


@admin.register(Vendor)
class VendorAdmin(ImportMixin, admin.ModelAdmin):
    list_filter = ["types", "subjects", GeolocationFilter]
    list_display = ["title", "address", "email", "phone", "on_map"]
    search_fields = ["title", "address", "email", "phone"]

    filter_horizontal = ["subjects", "types"]
    fields = [
        "title", "address", "geolocation", "phone", "email", "website", "description",
        "subjects", "types",
    ]

    formfield_overrides = {
        map_fields.AddressField: {
            "widget": map_widgets.GoogleMapsAddressWidget(attrs={"data-map-type": "roadmap"}),
        },
    }

    resource_class = VendorResource
    formats = (CustomCSV,)

    def on_map(self, vendor):
        return bool(vendor.geolocation)
    on_map.boolean = True
    on_map.short_description = "Added to map"


admin.site.register(Type)
admin.site.register(Subject)
