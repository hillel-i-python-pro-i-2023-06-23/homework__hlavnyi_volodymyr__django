import logging

from apps.crawler.models import Site


def delete_sites() -> None:
    logger = logging.getLogger("django")

    queryset = Site.objects.all()
    logger.info(f"Current amount of Sites before: {queryset.count()}")

    queryset_for_delete = queryset
    total_deleted, details = queryset_for_delete.delete()
    logger.info(f"Total deleted: {total_deleted}, details: {details}")

    logger.info(f"Current amount of Sites after: {queryset.count()}")
