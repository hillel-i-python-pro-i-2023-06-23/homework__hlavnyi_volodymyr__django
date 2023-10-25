# Docs: https://docs.djangoproject.com/en/3.2/topics/db/aggregation/
import logging

# from datetime import date

from django.db import models
from django.db.models import Avg, ExpressionWrapper, F, IntegerField
from django.db.models.functions import Now

from apps.contacts.models import Contact, GroupOfContact, TypeOfContact, InfoOfContact


# This procedure used for test purposes to
# show aggregation info about contacts
def show_aggregation_info():
    logger = logging.getLogger("django")
    logger.info("start")

    logger.info("Contacts base info =============================")
    data_set = get_info_about_all_group_count()
    for item in data_set:
        logger.info(f"{item=}")
    # logger.info(f"Total: {data_set}")

    logger.info("Contacts Group grouping =============================")
    data__grouping = get_contacts_group_grouping()

    for item in data__grouping:
        logger.info(f"{item=}")

    logger.info("Contacts Type grouping =============================")
    data__set = get_contacts_type_grouping()
    for item in data__set:
        # name_type = TypeOfContact.objects.get(pk=item["type"]).name
        logger.info(f"{item['group_name']} count={item['count']}")
    logger.info(f"Total type of detailed data of Contacts is {data__set.count()}")
    logger.info("===")
    dic_set = []
    for item in get_all_contacts_count_total_info():
        dic_set.append(item["contact_id"])
    logger.info(dic_set)
    logger.info("===")

    logger.info("Contact by id count info data =============================")
    query_contacts = Contact.objects.all()[:5]
    for cont in query_contacts:
        data__set = get_for_contact_type_by_id_grouping(cont.id)
        logger.info(f"Contact={cont.name}, count={data__set.count()}")
        for item in data__set:
            logger.info(f"{item}")
        #    name_type = TypeOfContact.objects.get(pk=item["type"]).name
        #    logger.info(f"Contact={cont.name}, name_type={name_type}, count={item['count']}")

    logger.info("Contact by id count info data =============================")
    query_contacts = Contact.objects.all()[:5]
    for cont in query_contacts:
        data__set = get_for_contact_count_total_info(cont.id)
        logger.info(f"Contact={cont.name}, count={data__set.count()}")
        # for item in data__set:
        #    logger.info(f"{item}")

    query_info = get_all_contacts_count_total_info()[:5]
    for item in query_info:
        logger.info(f"{item}")

    logger.info("Most Frequent Contacts Name ============================")
    query_contacts = get_most_frequent_contacts_name()
    logger.info(f"{query_contacts=}")
    for item in query_contacts:
        logger.info(f"Most frequent contacts name is {item=}")

    logger.info("Min Max Age Contact ============================")
    query_min_max = get_max_min_age_contact()
    logger.info(f"{query_min_max=}")
    # for item in query_min_max:
    #    logger.info(f"{item=}")

    logger.info("end")


def get_info_about_all_group_count():
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
    data = (
        queryset_contacts.annotate(group_name=models.F("groups_of_contact__name"))
        .values("group_name")
        .annotate(
            count=models.Count("group_name"),
        )
    )

    return data


def get_contacts_type_grouping():
    """
    Get contacts grouping by type name
    """
    queryset = InfoOfContact.objects.all()
    data = (
        queryset.annotate(group_name=models.F("type__name"))
        .values("group_name")
        .annotate(
            count=models.Count("group_name"),
        )
    )

    return data


def convert_to_dic_get_all_contacts_count_total_info():
    dic = []
    for item in get_all_contacts_count_total_info():
        dic.append(item["contact_id"])
    return dic


def get_for_contact_type_by_id_grouping(pk):
    """
    Get contacts grouping by type name
    """
    queryset = InfoOfContact.objects.filter(contact_id=pk)
    data = (
        queryset.annotate(
            type_name=models.F("type__name"),
        )
        .values("type__name")
        .order_by("type")
        .annotate(
            count=models.Count("id"),
        )
    )

    return data


def get_for_contact_count_total_info(pk):
    """
    Get contacts grouping by id and return total count
    """
    queryset = InfoOfContact.objects.filter(contact_id=pk)
    data = queryset.annotate(
        count=models.Count("id"),
    )

    return data


def get_all_contacts_count_total_info():
    """
    Get contacts grouping by id and return total count
    """
    queryset = InfoOfContact.objects.all()
    data = (
        queryset.values("contact_id")
        .order_by("contact_id")
        .annotate(
            contact_name=models.F("contact__name"),
            count=models.Count("id"),
        )
    )

    return data


def get_most_frequent_contacts_name():
    """
    Get contacts grouping by id and return total count
    """
    queryset_contacts = Contact.objects.all()
    data = (
        queryset_contacts.annotate(group_name=models.F("name"))
        .values("group_name")
        .annotate(
            count=models.Count("group_name"),
        )
        .order_by("-count")
    )

    return data[:3]


def get_age_from_date_of_birth(date_of_birth):
    """
    Get age from date of birth
    """
    from datetime import date

    today = date.today()
    if date_of_birth:
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return 0


def get_max_min_age_contact():
    """
    Get Max / Min contacts
    """
    queryset = Contact.objects.all()
    data = queryset.aggregate(
        date_of_birth_min=models.Max(
            models.ExpressionWrapper(models.F("date_of_birth"), output_field=models.DateField())
        ),
        date_of_birth_max=models.Min(
            models.ExpressionWrapper(models.F("date_of_birth"), output_field=models.DateField())
        ),
    )

    data["age_max"] = get_age_from_date_of_birth(data["date_of_birth_max"])
    data["age_min"] = get_age_from_date_of_birth(data["date_of_birth_min"])

    data["age_avg"] = (data["age_max"] - data["age_min"]) / 2

    return data


def get_avg_age_contact():
    """
    Get Max / Min contacts
    """

    # class YearDiff(models.Func):
    #     function = 'EXTRACT'
    #     template = "%(function)s(YEAR FROM %(expressions)s)"
    #
    # today = date.today()
    # age_expression = models.ExpressionWrapper(
    #     YearDiff(today, models.F('date_of_birth')),
    #     output_field=models.fields.IntegerField()
    # )
    # average_age = Contact.objects.annotate(age=age_expression).aggregate(avg_age=models.Avg('age'))

    # # Вычисляем средний возраст контактов
    # average_age = Contact.objects.aggregate(average_age=models.Avg("date_of_birth"))["average_age"]
    #
    # # Если нет записей с датами рождения, average_age будет None
    # if average_age is not None:
    #     # Преобразовываем средний возраст из timedelta в годы
    #     average_age_in_years = average_age.days / 365.25
    # else:
    #     # Обработка случая, когда нет данных о датах рождения
    #     average_age_in_years = None
    #
    # # Теперь average_age_in_years содержит средний возраст в годах

    data = Contact.objects.annotate(
        age_in_years=ExpressionWrapper(Now() - F("date_of_birth"), output_field=IntegerField())
    )

    average_age = data.aggregate(average_age=Avg("age_in_years"))["average_age"]

    return average_age
