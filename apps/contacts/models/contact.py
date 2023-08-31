from django.db import models

# For future setups
# from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    # Name
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    groups_of_contact = models.ManyToManyField(
        "GroupOfContact",
        related_name="contacts",
    )

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
        return self.name

    class Meta:
        ordering = ["-modified_at", "name"]
