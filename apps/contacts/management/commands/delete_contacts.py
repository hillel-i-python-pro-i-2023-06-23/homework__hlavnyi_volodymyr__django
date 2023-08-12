import logging

from django.core.management.base import BaseCommand

from apps.contacts.models import Contact


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--id", type=int, help="Which id contacts do you want to delete?", default=0)
        parser.add_argument("--all", type=str, help="Delete ALL contacts from table!", default="")

    def handle(self, *args, **options):
        id: int = options["id"]
        flag_all: str = options["all"]

        logger = logging.getLogger("django")

        queryset = Contact.objects.all()
        logger.info(f"Current amount of contacts before: {queryset.count()}")

        queryset_for_delete = queryset

        if not id == 0:
            total_deleted, details = queryset_for_delete.filter(pk=id).delete()

        if flag_all == "ALL":
            total_deleted, details = queryset_for_delete.all().delete()

        logger.info(f"Total deleted: {total_deleted}, details: {details}")

        logger.info(f"Current amount of contacts after: {queryset.count()}")
