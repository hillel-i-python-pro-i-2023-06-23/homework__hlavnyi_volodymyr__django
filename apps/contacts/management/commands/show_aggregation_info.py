import logging

from django.core.management.base import BaseCommand

# from django.db import models

from apps.contacts.models import TypeOfContact
from apps.contacts.services.aggregation import (
    get_contacts_group_grouping,
    get_contacts_type_grouping,
    get_base_info,
)


def show_aggregation_info():
    logger = logging.getLogger("django")
    logger.info("start")

    logger.info("Contacts base info =============================")
    data_set = get_base_info()
    for item in data_set:
        logger.info(f"{item=}")
    # logger.info(f"Total: {data_set}")

    logger.info("Contacts Group grouping =============================")
    data__grouping = get_contacts_group_grouping()

    for item in data__grouping:
        logger.info(f"{item=}")

    logger.info("Contacts Type grouping =============================")
    data__set = get_contacts_type_grouping()[:5]
    for item in data__set:
        name_type = TypeOfContact.objects.get(pk=item["type"]).name
        logger.info(f"{name_type=} count={item['count']}")
    logger.info(f"Total type of detailed data of Contacts is {data__set.count()}")

    # logger.info("Contact by id count info data =============================")
    # query_contacts = Contact.objects.all()[:5]
    # for cont in query_contacts:
    #     data__set = get_for_contact_type_by_id_grouping(cont.id)
    #     logger.info(f"Contact={cont.name}, count={data__set.count()}")
    #     for item in data__set:
    #         logger.info(f"{item}")
    #     #    name_type = TypeOfContact.objects.get(pk=item["type"]).name
    #     #    logger.info(f"Contact={cont.name}, name_type={name_type}, count={item['count']}")

    # logger.info("Contact by id count info data =============================")
    # query_contacts = Contact.objects.all()[:5]
    # for cont in query_contacts:
    #     data__set = get_for_contact_count_total_info(cont.id)
    #     logger.info(f"Contact={cont.name}, count={data__set.count()}")
    #     # for item in data__set:
    #     #    logger.info(f"{item}")

    # query_info = get_all_contacts_count_total_info()[:5]
    # for item in query_info:
    #     logger.info(f"{item}")

    logger.info("end")


class Command(BaseCommand):
    def handle(self, *args, **options):
        show_aggregation_info()
