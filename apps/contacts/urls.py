from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path("list/", views.ContactsListView.as_view(), name="contacts_list"),
    #
    path("delete/", views.delete_contacts_view, name="contacts_delete"),
    path("delete/<int:pk>/", views.ContactDeleteView.as_view(), name="contacts_delete"),
    #
    path("update/<int:pk>/", views.ContactUpdateView.as_view(), name="contacts_update"),
    #
    path("generate/", views.generate_contacts_view, name="contacts_generate"),
    #
    path("create/", views.ContactsCreateView.as_view(), name="contacts_create"),
    path("createdetails/<int:pk>/", views.ContactDetailCreateView.as_view(), name="contacts_details_create"),
    # path("createdetails/<int:pk>/", views.contact_info_detail_view, name="contacts_details_create"),
    #
    path("detail/<int:pk>/", views.ContactDetailView.as_view(), name="contacts_detail"),
    #
    # path("statistics/", views.StatisticsView.as_view(), name="contacts_statistics"),
]
