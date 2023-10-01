# from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from apps.contacts.forms import GenerateForm, ContactDetailForm
from apps.contacts.models import Contact, InfoOfContact
from apps.contacts.services.aggregation import (
    get_all_contacts_count_total_info,
    get_contacts_group_grouping,
    get_contacts_type_grouping,
    convert_to_dic_get_all_contacts_count_total_info,
    get_max_min_age_contact,
    get_most_frequent_contacts_name,
    get_info_about_all_group_count,
)
from apps.contacts.services.delete_contacts import delete_contacts
from apps.contacts.services.generate_and_save_contacts import generate_and_save_contacts


class ContactsListView(ListView):
    model = Contact
    context_object_name = "my_contacts_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["info_about_all_group_count_line_1_header"] = get_info_about_all_group_count()
        context["info_contacts_group_grouping_line_2_header"] = list(get_contacts_group_grouping())
        context["info_contacts_type_grouping_line_3_header"] = get_contacts_type_grouping()
        context["info_max_min_age_contact_line_4_header"] = get_max_min_age_contact()
        context["info_most_frequent_contacts_name_line_5_header"] = get_most_frequent_contacts_name()
        context["info_type_count_by_id_contact"] = get_all_contacts_count_total_info()
        context["info_type_count_by_id_contact_list_id"] = convert_to_dic_get_all_contacts_count_total_info()
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
            info_about_all_group_count_line_1_header=get_info_about_all_group_count(),
            info_contacts_group_grouping_line_2_header=list(get_contacts_group_grouping()),
            info_contacts_type_grouping_line_3_header=get_contacts_type_grouping(),
            info_max_min_age_contact_line_4_header=get_max_min_age_contact(),
            info_most_frequent_contacts_name_line_5_header=get_most_frequent_contacts_name(),
            info_type_count_by_id_contact=get_all_contacts_count_total_info(),
            info_type_count_by_id_contact_list_id=list(get_all_contacts_count_total_info().values("contact_id")),
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

    success_url = reverse_lazy("contacts:contacts_list")


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
