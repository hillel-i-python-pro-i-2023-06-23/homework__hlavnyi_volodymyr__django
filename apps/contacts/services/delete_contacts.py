import logging

from apps.contacts.models import Contact


def delete_contacts() -> None:
    logger = logging.getLogger("django")

    queryset = Contact.objects.all()
    logger.info(f"Current amount of contacts before: {queryset.count()}")

    queryset_for_delete = queryset
    # if is_only_auto_generated:
    #    logger.info("Delete only auto generated animals")
    #    queryset_for_delete = queryset_for_delete.filter(is_auto_generated=True)

    total_deleted, details = queryset_for_delete.delete()
    logger.info(f"Total deleted: {total_deleted}, details: {details}")

    logger.info(f"Current amount of contacts after: {queryset.count()}")
