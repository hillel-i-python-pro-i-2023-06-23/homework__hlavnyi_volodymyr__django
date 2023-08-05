from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView

# from django.views.generic import (CreateView, FormView)

from apps.contacts.forms import GenerateForm
from apps.contacts.models import Contact
from apps.contacts.services.delete_contacts import delete_contacts

from apps.contacts.services.generate_and_save_contacts import generate_and_save_contacts


class ContactsListView(ListView):
    model = Contact


def delete_contacts_view(request):
    delete_contacts()
    return redirect(reverse_lazy("contacts:contacts_list"))


class ContactDeleteView(DeleteView):
    model = Contact
    success_url = reverse_lazy("contacts:contacts_list")


class ContactUpdateView(UpdateView):
    model = Contact
    fields = (
        "name",
        "phone_number",
    )

    def get_success_url(self):
        # return reverse_lazy("contacts:contacts_update", kwargs=dict(pk=self.kwargs["pk"]))
        return reverse_lazy("contacts:contacts_list")


def generate_contacts_view(request):
    if request.method == "POST":
        form = GenerateForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]
            generate_and_save_contacts(amount=amount)
    else:
        form = GenerateForm()

    return render(
        request=request,
        template_name="contacts/contacts_generate.html",
        context=dict(
            contacts_list=Contact.objects.all(),
            form=form,
        ),
    )
