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
    for _ in range(faker.random_int(min=1, max=4)):
        add_group = GroupOfContact.objects.get(pk=faker.random_int(min=1, max=7))
        contact.groups_of_contact.add(add_group)


def add_random_info_of_contact(contact):
    for _ in range(faker.random_int(min=1, max=4)):
        add_type = TypeOfContact.objects.get(pk=faker.random_int(min=1, max=5))
        InfoOfContact(
            type=add_type,
            contact=contact,
            value=faker.phone_number(),
        ).save()


def generate_info_of_contact() -> InfoOfContact:
    return InfoOfContact(
        type=TypeOfContact.objects.get(pk=faker.random_int(min=1, max=5)),
        contact=Contact.objects.get(pk=faker.random_int(min=1, max=20)),
        value=faker.phone_number(),
    )


def generate_info_of_contacts(amount: int) -> Iterator[InfoOfContact]:
    for _ in range(amount):
        yield generate_info_of_contact()
