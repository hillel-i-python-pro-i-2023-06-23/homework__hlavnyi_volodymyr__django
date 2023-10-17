from .models import Site
from django import forms


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["url", "flag_was_finished_crawling"]


class CreateSiteForm(forms.Form):
    url_text = forms.CharField(label="Enter web site (start with https://)", required=True, initial="https://")
    flag_was_finished_crawling = forms.CheckboxInput()


class GetSatesListForm(forms.Form):
    sites_text = forms.CharField(
        widget=forms.Textarea,
        label="Enter sites",
        required=True,
        initial="https://example.com/"
        + "\r\n"
        + "https://www.djangoproject.com/"
        + "\r\n"
        + "https://www.facebook.com/"
        + "\r\n"
        + "https://www.wikipedia.org/"
        + "\r\n"
        + "https://ithillel.ua"
        + "\r\n"
        + "https://www.linkedin.com"
        + "\r\n"
        + "https://www.twitter.com/"
        + "\r\n"
        + "https://www.live.com/"
        + "\r\n"
        + "https://cambridge.ua"
        + "\r\n"
        + "https://www.codewars.com"
        + "\r\n"
        + "https://cnn.com"
        + "\r\n",
    )
