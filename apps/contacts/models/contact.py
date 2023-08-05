from django.db import models

# For future setups
# from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    # Name
    name = models.CharField(max_length=100)
    # Optional phone number
    # phone_number = PhoneNumberField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.name} {self.phone_number}"

    class Meta:
        ordering = ["-modified_at", "name"]
