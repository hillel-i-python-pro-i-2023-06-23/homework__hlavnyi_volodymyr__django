from apps.contacts.models import Contact, GroupOfContact, TypeOfContact, InfoOfContact
from django.db import models


def get_base_info():
    """
    Get base info about contacts
    """
    data = [
        {"group_name": "Contacts", "count": Contact.objects.count()},
        {"group_name": "Groups", "count": GroupOfContact.objects.count()},
        {"group_name": "Types", "count": TypeOfContact.objects.count()},
        {"group_name": "Details", "count": InfoOfContact.objects.count()},
    ]

    return data


def get_contacts_group_grouping():
    """
    Get contacts grouping by group name
    """
    queryset_contacts = Contact.objects.all()
    data__grouping = (
        queryset_contacts.annotate(group_name=models.F("groups_of_contact__name"))
        .values("group_name")
        .annotate(
            count=models.Count("group_name"),
        )
    )

    return data__grouping


def get_contacts_type_grouping():
    """
    Get contacts grouping by type name
    """
    queryset = InfoOfContact.objects.all()
    data__set = (
        queryset.annotate(group_name=models.F("type__name"))
        .values("group_name")
        .annotate(
            count=models.Count("group_name"),
        )
    )

    return data__set


def convert_to_dic_get_all_contacts_count_total_info():
    dic_set = []
    for item in get_all_contacts_count_total_info():
        dic_set.append(item["contact_id"])
    return dic_set


def get_for_contact_type_by_id_grouping(pk):
    """
    Get contacts grouping by type name
    """
    queryset = InfoOfContact.objects.filter(contact_id=pk)
    data__set = (
        queryset.annotate(
            type_name=models.F("type__name"),
        )
        .values("type__name")
        .order_by("type")
        .annotate(
            count=models.Count("id"),
        )
    )

    return data__set


def get_for_contact_count_total_info(pk):
    """
    Get contacts grouping by id and return total count
    """
    queryset = InfoOfContact.objects.filter(contact_id=pk)
    data__set = queryset.annotate(
        count=models.Count("id"),
    )

    return data__set


def get_all_contacts_count_total_info():
    """
    Get contacts grouping by id and return total count
    """
    queryset = InfoOfContact.objects.all()
    data__set = (
        queryset.values("contact_id")
        .order_by("contact_id")
        .annotate(
            contact_name=models.F("contact__name"),
            count=models.Count("id"),
        )
    )

    return data__set


def get_most_frequent_contacts_name():
    """
    Get contacts grouping by id and return total count
    """
    queryset = Contact.objects.all()
    data__set = (
        queryset.values("name")
        .annotate(
            count=models.Count("name"),
        )
        .order_by("count")
    )

    return data__set
