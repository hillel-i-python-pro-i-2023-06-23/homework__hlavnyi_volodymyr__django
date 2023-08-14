from django.contrib import admin
from apps.contacts import models


# admin.site.register(models.Contact)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "created_at",
        "modified_at",
        "name",
        "phone_number",
    )
