from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .models import Vendor, Subject, Type


def vendor_list(request):
    """
    Basic template view to render the app skeleton
    """
    context = {
        "types": Type.objects.all(),
        "subjects": Subject.objects.all(),
        "vendor_count": Vendor.objects.exclude(geolocation="").count()
    }
    return render(request, "vendors/vendor_list.html", context)


@cache_page(60)
def vendor_list_json(request):
    """
    JSON representation of vendors to populate the app
    """
    vendors = []
    for vendor in Vendor.objects.exclude(geolocation=""):
        vendors.append({
            "id": vendor.id,
            "title": vendor.title,
            "address": vendor.address,
            "description": vendor.description,
            "phone": vendor.phone,
            "email": vendor.email,
            "website": vendor.website,
            "types": list(vendor.types.values_list("id", flat=True)),
            "subjects": list(vendor.subjects.values_list("id", flat=True)),
            "position": {
                "lat": vendor.geolocation.lat,
                "lng": vendor.geolocation.lon,  # Google Maps expect "lng", not "lon"
            },
        })
    return JsonResponse(vendors, safe=False)
