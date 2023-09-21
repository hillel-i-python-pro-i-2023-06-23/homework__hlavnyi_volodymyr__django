# Docs: https://docs.djangoproject.com/en/3.2/topics/db/aggregation/

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
    data__set = queryset.annotate(
        name_contact=models.F("name"),
        count_name=models.Count("name"),
    ).aggregate(models.Sum("count_name"))

    return data__set


def get_age_from_date_of_birth(date_of_birth):
    """
    Get age from date of birth
    """
    from datetime import date

    today = date.today()
    if date_of_birth:
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return None


def get_max_min_age_contact():
    """
    Get Max / Min contacts
    """
    queryset = Contact.objects.all()
    data__set = queryset.aggregate(
        date_of_birth_min=models.Max(
            models.ExpressionWrapper(models.F("date_of_birth"), output_field=models.DateField())
        ),
        date_of_birth_max=models.Min(
            models.ExpressionWrapper(models.F("date_of_birth"), output_field=models.DateField())
        ),
    )

    data__set["age_max"] = get_age_from_date_of_birth(data__set["date_of_birth_max"])
    data__set["age_min"] = get_age_from_date_of_birth(data__set["date_of_birth_min"])

    # data__set_avg = (queryset
    #         .aggregate(
    #         date_of_birth_avg=models.Avg(
    #             models.ExpressionWrapper(models.F('date_of_birth'),
    #                                         output_field=models.IntegerField())),
    #     )
    # )

    data__set["age_avg"] = (data__set["age_max"] - data__set["age_min"]) / 2
    # get_age_from_date_of_birth(data__set_avg["date_of_birth_avg"])

    return data__set
