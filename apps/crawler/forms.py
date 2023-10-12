from .models import Site
from django import forms


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["url", "flag_was_finished_crawling"]


class GetSatesListForm(forms.Form):
    sites_text = forms.CharField(
        widget=forms.Textarea,
        label="Enter sites",
        required=True,
        initial="https://www.google.com/"
        + "\r\n"
        + "https://www.youtube.com/"
        + "\r\n"
        + "https://www.facebook.com/"
        + "\r\n"
        + "https://www.wikipedia.org/"
        + "\r\n"
        + "https://www.reddit.com/"
        + "\r\n"
        + "https://www.amazon.com/"
        + "\r\n"
        + "https://www.yahoo.com/"
        + "\r\n"
        + "https://www.twitter.com/"
        + "\r\n"
        + "https://www.live.com/"
        + "\r\n",
    )
