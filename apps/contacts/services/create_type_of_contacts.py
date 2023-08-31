from apps.contacts.models import TypeOfContact


def create_type_of_contact(name) -> TypeOfContact:
    return TypeOfContact(name=name)


def create_type_of_contacts(list_of_type_of_contacts=None):
    if list_of_type_of_contacts is None:
        list_of_type_of_contacts = ["Phone", "Email", "LinkedIn", "Telegram", "Other"]

    for list_name in list_of_type_of_contacts:
        create_type_of_contact(name=list_name).save()
