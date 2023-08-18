from django.contrib import admin
from apps.contacts import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date_of_birth",
        # "list_of_contacts"
        "created_at",
        "modified_at",
    )

    list_filter = (
        "name",
        "date_of_birth",
        "created_at",
        "modified_at",
    )

    def list_of_contacts(self, obj):
        return super().get_queryset(self).select_related("info_of_contact")


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


@admin.register(models.TypeOfContact)
class TypeOfContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "modified_at",
    )


@admin.register(models.InfoOfContact)
class InfoOfContactAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "value",
        "created_at",
        "modified_at",
    )
