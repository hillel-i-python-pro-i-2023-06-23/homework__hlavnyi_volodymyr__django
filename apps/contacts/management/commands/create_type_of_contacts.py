import logging

from django.core.management.base import BaseCommand

from apps.contacts import models
from apps.contacts.services.create_type_of_contacts import create_type_of_contacts


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger("django")

        queryset = models.TypeOfContact.objects.all()

        logger.info(f"Current amount of Type of Contacts before: {queryset.count()}")

        create_type_of_contacts()

        logger.info(f"Current amount of Type of contacts after: {queryset.count()}")
