from django.core.management.base import BaseCommand

# from django.db import models
from apps.contacts.services.aggregation import get_avg_age_contact


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(f"Show average age of contacts {get_avg_age_contact()=}")
        # for item in get_avg_age_contact():
        #    print(f"{item=} {item.age}")
