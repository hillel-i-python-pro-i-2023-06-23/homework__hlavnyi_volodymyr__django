import logging

from apps.contacts.models import Contact


def delete_contacts() -> None:
    logger = logging.getLogger("django")

    queryset = Contact.objects.all()
    logger.info(f"Current amount of contacts before: {queryset.count()}")

    queryset_for_delete = queryset
    total_deleted, details = queryset_for_delete.delete()
    logger.info(f"Total deleted: {total_deleted}, details: {details}")

    logger.info(f"Current amount of contacts after: {queryset.count()}")
