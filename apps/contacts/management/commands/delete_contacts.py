import logging

from django.core.management.base import BaseCommand

from apps.contacts.models import Contact


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--id", type=int, help="Which id contacts do you want to delete?", default=0)
        parser.add_argument("--all", action="store_true", help="Delete ALL contacts from table!", default="")

    def handle(self, *args, **options):
        id_number: int = options["id"]
        flag_all: str = options["all"]

        logger = logging.getLogger("django")

        queryset = Contact.objects.all()
        logger.info(f"Current amount of contacts before: {queryset.count()}")

        queryset_for_delete = queryset

        if id_number != 0:
            total_deleted, details = queryset_for_delete.filter(pk=id_number).delete()

        if flag_all is True:
            total_deleted, details = queryset_for_delete.all().delete()

        logger.info(f"Total deleted: {total_deleted}, details: {details}")

        logger.info(f"Current amount of contacts after: {queryset.count()}")
