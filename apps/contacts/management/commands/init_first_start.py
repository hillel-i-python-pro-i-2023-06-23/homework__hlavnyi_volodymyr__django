import logging

from django.core.management.base import BaseCommand

from apps.contacts import models
from apps.contacts.management.commands.generate_contacts import generate_contacts
from apps.contacts.services.create_group_of_contacts import create_group_of_contacts
from apps.contacts.services.create_type_of_contacts import create_type_of_contacts


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Contacts (20 pcs)
        init_first_contacts(amount=20)

        # Group of Contacts
        init_first_group_of_contacts(["Family", "Friend", "Children", "Job", "Special 2023", "School", "Other"])

        # Type of Contacts
        init_first_type_of_contacts(["Phone", "Email", "LinkedIn", "Telegram", "Other"])


# Contacts (20 pcs)
def init_first_contacts(amount: int = 10) -> None:
    logger = logging.getLogger("django")

    queryset = models.Contact.objects.all()

    logger.info(f"Current amount of Contacts before: {queryset.count()}")

    if queryset.count() == 0:
        generate_contacts(amount=amount)
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
