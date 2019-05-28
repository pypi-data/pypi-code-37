from django.core.management.base import BaseCommand
from django_stomp.publisher import build_publisher


class Command(BaseCommand):
    help = "Start internal PUB/SUB logic"

    def handle(self, *args, **options):
        publisher = build_publisher("fake_client_id")

        publisher.send({}, "test_send_queue")
