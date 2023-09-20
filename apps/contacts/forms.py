from django import forms
from django.forms import ModelForm

from apps.contacts.models import Contact
from apps.contacts.models import InfoOfContact


# from apps.contacts.models import TypeOfContact


class GenerateForm(forms.Form):
    amount = forms.IntegerField(
        label="Amount",
        min_value=1,
        max_value=300,
        required=True,
        initial=5,
    )


class ContactSpecialEditForm(forms.ModelForm):
    class Meta:
        model = Contact

        fields = (
            "name",
            # "phone_number",
        )


class ContactForm(ModelForm):
    class Meta:
        model = InfoOfContact
        fields = ["type", "value"]


class ContactDetailForm(forms.ModelForm):
    class Meta:
        model = InfoOfContact

        fields = (
            "contact",
            "type",
            "value",
        )


class StatisticsForm(forms.Form):
    pass
