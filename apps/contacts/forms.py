from django import forms

from apps.contacts.models import Contact


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
            "phone_number",
        )
