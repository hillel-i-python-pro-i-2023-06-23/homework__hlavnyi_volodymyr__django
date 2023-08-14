from collections.abc import Iterator

from faker import Faker

from apps.contacts.models import Contact

faker = Faker()


def generate_contact() -> Contact:
    return Contact(
        name=faker.first_name(),
        # phone_number=faker.phone_number(),
        phone_number=f"{faker.country_calling_code()}{faker.msisdn()}",
    )


def generate_contacts(amount: int) -> Iterator[Contact]:
    for _ in range(amount):
        yield generate_contact()
