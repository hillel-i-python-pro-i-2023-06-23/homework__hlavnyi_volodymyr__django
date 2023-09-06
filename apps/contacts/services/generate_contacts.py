from collections.abc import Iterator

from faker import Faker

from apps.contacts.models import Contact, InfoOfContact, TypeOfContact, GroupOfContact


faker = Faker()


def generate_contact() -> Contact:
    if faker.pybool(1):
        date_of_birth = None
    else:
        date_of_birth = faker.date_of_birth()

    return Contact(
        name=faker.first_name(),
        date_of_birth=date_of_birth,
    )


def generate_contacts(amount: int) -> Iterator[Contact]:
    for _ in range(amount):
        yield generate_contact()


def add_random_groups(contact):
    for _ in range(faker.random_int(min=1, max=GroupOfContact.objects.count())):
        add_group = GroupOfContact.objects.order_by("?").first()
        contact.groups_of_contact.add(add_group)


def add_random_info_of_contact(contact):
    for _ in range(faker.random_int(min=1, max=TypeOfContact.objects.count())):
        add_type = TypeOfContact.objects.order_by("?").first()
        InfoOfContact(
            type=add_type,
            contact=contact,
            value=faker.phone_number(),
        ).save()


def generate_info_of_contact() -> InfoOfContact:
    return InfoOfContact(
        type=TypeOfContact.objects.order_by("?").first(),
        contact=Contact.objects.order_by("?").first(),
        value=faker.phone_number(),
    )


def generate_info_of_contacts(amount: int) -> Iterator[InfoOfContact]:
    for _ in range(amount):
        yield generate_info_of_contact()
