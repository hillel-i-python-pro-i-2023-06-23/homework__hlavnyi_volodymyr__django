from apps.contacts.models import GroupOfContact


def create_group_of_contact(name) -> GroupOfContact:
    return GroupOfContact(name=name)


def create_group_of_contacts(list_of_group_of_contacts=None):
    if list_of_group_of_contacts is None:
        list_of_group_of_contacts = ["Family", "Friend", "Children", "Job", "Special 2023", "School", "Other"]

    for list_name in list_of_group_of_contacts:
        create_group_of_contact(name=list_name).save()
