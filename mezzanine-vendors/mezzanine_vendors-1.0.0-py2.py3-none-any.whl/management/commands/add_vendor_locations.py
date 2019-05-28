from __future__ import absolute_import, unicode_literals

import googlemaps

from django.conf import settings
from django.core.management.base import BaseCommand

from vendors.models import Vendor


class Command(BaseCommand):
    help = "Perform a geocoder query for each Vendor without a set location"

    def handle(self, *args, **options):
        processed = 0
        failed = 0
        api = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        for vendor in Vendor.objects.filter(geolocation=""):
            self.stdout.write("Processing {}".format(vendor))
            try:
                result = api.geocode(vendor.address)
            except googlemaps.exceptions.ApiError as e:
                failed += 1
                self.stderr.write("API error ({}) when processing {}".format(e, vendor))
                continue

            if len(result) == 0:
                failed += 1
                self.stderr.write("Error: No geolocation results found for {}".format(vendor))
                continue

            vendor.geolocation.lat = result[0]["geometry"]["location"]["lat"]
            vendor.geolocation.lon = result[0]["geometry"]["location"]["lng"]
            vendor.save()
            processed += 1

        self.stdout.write("Processed: {}".format(processed))
        self.stdout.write("Failed: {}".format(failed))
