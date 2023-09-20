# from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from apps.contacts.forms import GenerateForm, ContactDetailForm
from apps.contacts.models import Contact, InfoOfContact
from apps.contacts.services.aggregation import get_all_contacts_count_total_info, get_base_info
from apps.contacts.services.delete_contacts import delete_contacts
from apps.contacts.services.generate_and_save_contacts import generate_and_save_contacts


# FormView)


class ContactsListView(ListView):
    model = Contact
    context_object_name = "my_contacts_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["extra_info_1"] = get_base_info()
        context["extra_info_2"] = get_base_info()
        context["extra_info_type_count_by_id_contact"] = get_all_contacts_count_total_info()
        return context


class ContactDetailView(DetailView):
    model = Contact

    # queryset = InfoOfContact.objects.filter(Contacts__pk=Contact.pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["info_of_contact"] = InfoOfContact.objects.filter(contact_id=self.kwargs["pk"])
        return context


class ContactsCreateView(CreateView):
    model = Contact
    fields = (
        "name",
        "date_of_birth",
        "groups_of_contact",
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
        "date_of_birth",
        "groups_of_contact",
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


class ContactDetailCreateView(DetailView):
    model = InfoOfContact
    form_class = ContactDetailForm
    template_name = "contacts/infoofcontact_form.html"
    fields = (
        "contact",
        "type",
        "value",
    )

    # readonly_fields = ("contact",)

    # def get_initial(self):
    #    initial = super().get_initial()
    # initial["contact"] = self.kwargs["pk"]
    # initial["instance"] = InfoOfContact.objects.get(contact_id=self.kwargs["pk"])
    # initial["contact"] = Contact.objects.get(pk=self.kwargs["pk"])
    #    return initial

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    # context["instance"] = InfoOfContact.objects.get(pk=self.kwargs["pk"])
    # context["instance"].contact = InfoOfContact.objects.get(pk=self.kwargs["pk"]).contact
    #    return context

    # def get_success_url(self):
    #    return reverse_lazy("contacts:contacts_detail", kwargs=dict(pk=self.kwargs["pk"]))
    # success_url = reverse_lazy("contacts:contacts_detail", kwargs=dict(pk=self.kwargs["pk"]))
    success_url = reverse_lazy("contacts:contacts_list")
    # return reverse_lazy("contacts:contacts_list")


def contact_info_detail_view(request, pk):
    contact = Contact.objects.get(pk=pk)
    info_of_contact = InfoOfContact.objects.filter(contact_id=pk)

    if request.method == "POST":
        form = ContactDetailForm(request.POST)

        if form.is_valid():
            form.save()
            # return redirect(reverse_lazy("contacts:contacts_detail", kwargs=dict(pk=pk)))
            needed_html = "contacts/contact_detail.html"
        else:
            needed_html = "contacts/infoofcontact_form.html"

    else:
        form = ContactDetailForm()
        needed_html = "contacts/infoofcontact_form.html"

    return render(
        request=request,
        template_name=needed_html,
        context=dict(
            contact=contact,
            info_of_contact=info_of_contact,
        ),
    )
