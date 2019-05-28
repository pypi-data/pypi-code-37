from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.vendor_list, name="list"),
    url(r"^json/$", views.vendor_list_json, name="list_json"),
]
