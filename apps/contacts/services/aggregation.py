from apps.contacts.models import Contact, InfoOfContact
from django.db import models


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
        queryset.annotate(type_name=models.F("type"))
        .values("type")
        .annotate(
            count=models.Count("type"),
        )
    )

    return data__set
