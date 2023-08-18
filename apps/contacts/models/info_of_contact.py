from django.db import models


class InfoOfContact(models.Model):
    """
    Info of contacts.
    For example:
        - phone - number
        - email - string
        - LinkedIn - url
        - telegram - string
        - other social networks - url
        - etc.
        AND
        Value of info.
    """

    type = models.ForeignKey(
        "TypeOfContact",
        on_delete=models.CASCADE,
        related_name="type_of_contacts",
    )

    contact = models.ForeignKey(
        "Contact",
        on_delete=models.CASCADE,
        related_name="info_list_of_contact",
    )

    value = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.type}: {self.value}"

    __repr__ = __str__
