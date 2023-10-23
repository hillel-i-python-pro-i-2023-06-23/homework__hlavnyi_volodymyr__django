from django.core.management.base import BaseCommand

# from django.db import models
from apps.contacts.services.aggregation import show_aggregation_info


class Command(BaseCommand):
    def handle(self, *args, **options):
        show_aggregation_info()
