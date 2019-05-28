from __future__ import absolute_import, unicode_literals

from django.db import models
from django_google_maps import fields as map_fields

from mezzanine.core.models import TimeStamped

from mezzy.utils.models import Titled


class Subject(Titled):
    """
    A subject to group vendors
    """


class Type(Titled):
    """
    A type to group vendors
    """


class Vendor(TimeStamped, Titled):
    """
    A vendor that offers product / services to parents
    """
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    phone = models.CharField("Phone", max_length=100)
    email = models.EmailField("Email", max_length=254)
    website = models.CharField("Website", max_length=100, blank=True)
    description = models.TextField("Description", blank=True)

    subjects = models.ManyToManyField(Subject, related_name="vendors")
    types = models.ManyToManyField(Type, related_name="vendors")

    class Meta:
        ordering = ["title"]
