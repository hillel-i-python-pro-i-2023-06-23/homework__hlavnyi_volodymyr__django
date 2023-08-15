from django.contrib import admin
from apps.contacts import models


# admin.site.register(models.Contact)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "date_of_birth",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "name",
        "phone_number",
        "date_of_birth",
        "created_at",
        "modified_at",
    )


@admin.register(models.GroupOfContact)
class GroupOfContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "modified_at",
        #
        "amount_of_contacts",
        #
    )
