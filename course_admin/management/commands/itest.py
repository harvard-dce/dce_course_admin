from django.core.management.base import BaseCommand, CommandError
from docker import Client as DockerClient

class Command(BaseCommand):
        def handle(self, *args, **options):
                pass
