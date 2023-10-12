from .models import Site
from django import forms


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["url", "flag_was_finished_crawling"]
