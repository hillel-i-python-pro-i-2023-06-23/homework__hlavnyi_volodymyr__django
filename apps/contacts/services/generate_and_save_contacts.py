import logging

from apps.contacts.models import Contact
from apps.contacts.services.generate_contacts import generate_contacts, add_random_groups, add_random_info_of_contact


def generate_and_save_contacts(amount: int) -> None:
    logger = logging.getLogger("django")

    queryset = Contact.objects.all()

    logger.info(f"Current amount of contacts before: {queryset.count()}")

    for contact in generate_contacts(amount=amount):
        contact.save()
        add_random_groups(contact=contact)
        add_random_info_of_contact(contact=contact)

    logger.info(f"Current amount of contacts after: {queryset.count()}")
