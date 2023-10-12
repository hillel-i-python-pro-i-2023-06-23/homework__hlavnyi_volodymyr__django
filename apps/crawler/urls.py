from django.urls import path

from . import views

app_name = "crawler"

urlpatterns = [
    path("sites_list/", views.SitesListView.as_view(), name="sites_list"),
    path("site_create/", views.SiteCreateView.as_view(), name="site_create"),
    path("site_edit/<int:site_id>", views.site_edit, name="site_edit"),
    path("site_delete/<int:site_id>", views.site_delete, name="site_delete"),
    #
    path("sites_enter/", views.get_sites_list_view, name="sites_enter"),
    # path("delete/", views.delete_contacts_view, name="contacts_delete"),
    # path("delete/<int:pk>/", views.ContactDeleteView.as_view(), name="contacts_delete"),
    #
]
