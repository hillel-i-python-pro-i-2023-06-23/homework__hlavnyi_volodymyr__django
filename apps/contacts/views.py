from django.views.generic import ListView

from apps.contacts.models import Contact


class ContactsListView(ListView):
    model = Contact
