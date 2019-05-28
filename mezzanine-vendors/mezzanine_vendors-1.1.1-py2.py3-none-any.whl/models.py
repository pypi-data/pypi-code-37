from __future__ import absolute_import, unicode_literals

import googlemaps

from django.db import models
from django_google_maps import fields as map_fields
from django.utils.timezone import now

from mezzanine.conf import settings
from mezzanine.core.models import TimeStamped

from mezzy.utils.models import Titled


class GeolocationError(Exception):
    """
    Indicates a problem when performing geolocation queries for a vendor.
    """


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
    geolocation_updated = models.DateTimeField(blank=True, null=True)

    phone = models.CharField("Phone", max_length=100)
    email = models.EmailField("Email", max_length=254)
    website = models.CharField("Website", max_length=100, blank=True)
    description = models.TextField("Description", blank=True)

    subjects = models.ManyToManyField(Subject, related_name="vendors")
    types = models.ManyToManyField(Type, related_name="vendors")

    class Meta:
        ordering = ["title"]

    def update_geolocation(self, force=False):
        """
        Attempt to get new coordinates based on a vendor's address.
        """
        # Skip vendors with a failed attempt that haven't been updated since
        if not force:
            if self.geolocation_updated and self.geolocation_updated >= self.updated:
                raise GeolocationError(
                    "Vendor {} has not been updated since last geocode attempt".format(self))

        error = None
        api = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        try:
            result = api.geocode(self.address)
            self.geolocation.lat = result[0]["geometry"]["location"]["lat"]
            self.geolocation.lon = result[0]["geometry"]["location"]["lng"]
        except googlemaps.exceptions.ApiError as e:
            error = "API error ({}) when processing {}".format(e, self)
        except IndexError:
            error = "No geolocation results found for {}".format(self)

        self.geolocation_updated = now()
        self.save()

        if error:
            raise GeolocationError(error)
