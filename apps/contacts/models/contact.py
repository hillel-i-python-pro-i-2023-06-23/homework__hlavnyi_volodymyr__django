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

    @property
    def groups_of_contact_amount(self):
        return self.groups_of_contact.count()

    @property
    def age(self):
        from datetime import date

        today = date.today()
        if self.date_of_birth:
            return (
                today.year
                - self.date_of_birth.year
                - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            )
        return None

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
