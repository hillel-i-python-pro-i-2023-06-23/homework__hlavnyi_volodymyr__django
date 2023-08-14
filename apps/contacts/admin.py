from django.contrib import admin
from apps.contacts import models


# admin.site.register(models.Contact)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "group_of_contact",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "name",
        "phone_number",
        "created_at",
        "modified_at",
    )


@admin.register(models.Group_of_contact)
class Group_of_contactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "name",
        #
        #
        "created_at",
        "modified_at",
    )
