import logging

from django.core.management.base import BaseCommand

# from django.db import models

from apps.contacts.models import Contact, GroupOfContact, TypeOfContact, InfoOfContact
from apps.contacts.services.aggregation import (
    get_contacts_group_grouping,
    get_contacts_type_grouping,
    get_for_contact_by_id_grouping,
)


def show_aggregation_info():
    logger = logging.getLogger("django")
    logger.info("start")

    logger.info(f"contacts: {Contact.objects.count()}")
    logger.info(f"groups of contacts: {GroupOfContact.objects.count()}")
    logger.info(f"types of contacts: {TypeOfContact.objects.count()}")
    logger.info(f"info of contacts: {InfoOfContact.objects.count()}")

    logger.info("Contacts Group grouping =============================")
    data__grouping = get_contacts_group_grouping()

    for item in data__grouping:
        logger.info(f"{item=}")

    logger.info("Contacts Type grouping =============================")
    data__set = get_contacts_type_grouping()
    for item in data__set:
        name_type = TypeOfContact.objects.get(pk=item["type"]).name
        logger.info(f"{name_type=} count={item['count']}")

    logger.info("Contact by id count info data =============================")
    queryContacts = Contact.objects.all()
    for cont in queryContacts:
        data__set = get_for_contact_by_id_grouping(cont.id)
        for item in data__set:
            logger.info(f"Contact={cont.name}, item={item}")
        #    name_type = TypeOfContact.objects.get(pk=item["type"]).name
        #    logger.info(f"Contact={cont.name}, name_type={name_type}, count={item['count']}")


class Command(BaseCommand):
    def handle(self, *args, **options):
        show_aggregation_info()
