import logging

from apps.contacts.models import Contact

# from apps.contacts.services.generate_contacts import generate_contacts


def generate_and_save_contacts(amount: int) -> None:
    logger = logging.getLogger("django")

    queryset = Contact.objects.all()

    logger.info(f"Current amount of contacts before: {queryset.count()}")

    #    for contact in generate_contacts(amount=amount):
    #        animal.is_auto_generated = True
    #        animal.save()

    logger.info(f"Current amount of contacts after: {queryset.count()}")
