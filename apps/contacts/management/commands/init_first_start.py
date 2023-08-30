import logging

from django.core.management.base import BaseCommand

from apps.contacts import models
from apps.contacts.management.commands.generate_contacts import generate_contacts
from apps.contacts.services.create_group_of_contacts import create_group_of_contacts
from apps.contacts.services.create_type_of_contacts import create_type_of_contacts
from apps.contacts.services.generate_contacts import add_random_groups, add_random_info_of_contact


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger = logging.getLogger("django")

        # 1st Group of Contacts
        logger.info("---------Start filling the database with the 1st step")
        init_first_group_of_contacts(["Family", "Friend", "Children", "Job", "Special 2023", "School", "Other"])
        logger.info("---------Finish filling the database with the 1st step")

        # 2nd Type of Contacts
        logger.info("---------Start filling the database with the 2nd step")
        init_first_type_of_contacts(["Phone", "Email", "LinkedIn", "Telegram", "Other"])
        logger.info("---------Finish filling the database with the 2nd step")

        # 3rd Contacts
        # Contacts (20 pcs)
        logger.info("---------Start filling the database with the 3rd step")
        init_first_contacts(amount=20)
        logger.info("---------Finish filling the database with the 3rd step")


# Contacts (20 pcs)
def init_first_contacts(amount: int = 10) -> None:
    logger = logging.getLogger("django")

    queryset = models.Contact.objects.all()

    logger.info(f"Current amount of Contacts before: {queryset.count()}")

    if queryset.count() == 0:
        for contact in generate_contacts(amount=amount):
            contact.save()
            # add extra fields randomly
            add_random_groups(contact=contact)
            add_random_info_of_contact(contact=contact)
        logger.info(f"Create new Contacts (amount is {amount})")
    else:
        logger.info(f"Contacts already exists (current amount is {queryset.count()}). Skip creating new Contacts!")


def init_first_type_of_contacts(list_group) -> None:
    logger = logging.getLogger("django")

    queryset = models.TypeOfContact.objects.all()

    logger.info(f"Current amount of Type of Contacts before: {queryset.count()}")

    if queryset.count() == 0:
        create_type_of_contacts(list_of_type_of_contacts=list_group)
        logger.info(f"Current amount of Type of contacts after: {queryset.count()}")
    else:
        logger.info(
            f"Contacts already exists (current amount is {queryset.count()})." f" Skip creating new Type of Contacts!"
        )


def init_first_group_of_contacts(list_group) -> None:
    logger = logging.getLogger("django")

    queryset = models.GroupOfContact.objects.all()

    logger.info(f"Current amount of Group of Contacts before: {queryset.count()}")

    if queryset.count() == 0:
        create_group_of_contacts(list_of_group_of_contacts=list_group)
        logger.info(f"Current amount of Group of contacts after: {queryset.count()}")
    else:
        logger.info(
            f"Groups already exists (current amount is {queryset.count()})." f" Skip creating new Groups of Contacts!"
        )
