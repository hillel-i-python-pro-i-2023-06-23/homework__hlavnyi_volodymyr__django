from django.db import models


class GroupOfContact(models.Model):
    """
    Group of contacts.
    For example:
        - Family
        - Friends
        - etc.
    """

    name = models.CharField(max_length=150, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def amount_of_contacts(self):
        return self.contacts.count()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    __repr__ = __str__
