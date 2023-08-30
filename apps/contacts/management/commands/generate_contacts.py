import logging

from django.core.management.base import BaseCommand

from apps.contacts.models import Contact
from apps.contacts.services.generate_contacts import generate_contacts
from apps.contacts.services.generate_contacts import add_random_groups, add_random_info_of_contact


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--amount",
            type=int,
            help="How many contacts do you want to generate?",
            default=10,
        )

    def handle(self, *args, **options):
        amount: int = options["amount"]

        # is_mark_as_autogenerated

        logger = logging.getLogger("django")

        queryset = Contact.objects.all()

        logger.info(f"Current amount of animals before: {queryset.count()}")

        for contact in generate_contacts(amount=amount):
            contact.save()
            add_random_groups(contact=contact)
            add_random_info_of_contact(contact=contact)

        logger.info(f"Current amount of contacts after: {queryset.count()}")
