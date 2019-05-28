from __future__ import absolute_import, unicode_literals

from django.core.management.base import BaseCommand

from vendors.models import Vendor, GeolocationError


class Command(BaseCommand):
    help = "Perform a geocoder query for each Vendor without a set location"

    def handle(self, *args, **options):
        processed = 0
        failed = 0

        for vendor in Vendor.objects.filter(geolocation=""):
            self.stdout.write("Processing {}".format(vendor))
            try:
                vendor.update_geolocation()
            except GeolocationError as e:
                failed += 1
                self.stderr.write(str(e))
            else:
                processed += 1

        self.stdout.write("Processed: {}".format(processed))
        self.stdout.write("Failed: {}".format(failed))
