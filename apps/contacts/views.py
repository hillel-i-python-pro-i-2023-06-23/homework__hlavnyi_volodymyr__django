from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, DetailView

from django.views.generic import CreateView

from apps.contacts.forms import GenerateForm
from apps.contacts.models import Contact, InfoOfContact
from apps.contacts.services.delete_contacts import delete_contacts

from apps.contacts.services.generate_and_save_contacts import generate_and_save_contacts


class ContactsListView(ListView):
    model = Contact
    context_object_name = "my_contacts_list"
    # context_object_name = "my_favorite_publishers"
    # queryset = Contact.objects.all()
    # template_name = "contacts/contact_list.html"


# class ContactsDetailView(DetailView):
#    context_object_name = "contacts_list"
#    queryset = InfoOfContact.objects.all()


# class AcmeBookListView(ListView):
#    context_object_name = "book_list"
#    queryset = Book.objects.filter(publisher__name="ACME Publishing")
#    template_name = "books/acme_list.html"


class ContactDetailView(DetailView):
    model = Contact

    # queryset = InfoOfContact.objects.filter(Contacts__pk=Contact.pk)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # kwargs["instance"] = Animal.objects.get(pk=self.kwargs["pk"])
        context["info_of_contacts"] = InfoOfContact.objects.filter(contact_id=self.kwargs["pk"])

        return context


class ContactsCreateView(CreateView):
    model = Contact
    fields = (
        "name",
        # "phone_number",
    )
    success_url = reverse_lazy("contacts:contacts_list")


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
        # "phone_number",
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
