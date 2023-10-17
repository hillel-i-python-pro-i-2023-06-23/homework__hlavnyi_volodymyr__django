from django.urls import path

from . import views

app_name = "crawler"

urlpatterns = [
    path("sites_list/", views.SitesListView.as_view(), name="sites_list"),
    path("site_create/", views.site_create_view, name="site_create"),
    path("site_edit/<int:site_id>", views.site_edit, name="site_edit"),
    path("site_delete/<int:site_id>", views.site_delete, name="site_delete"),
    path("delete_all/", views.delete_sites_all_view, name="sites_delete_all"),
    #
    path("sites_enter/", views.get_sites_list_view, name="sites_enter"),
    path("sites_start_crawling/", views.start_crawling_sites_all_view, name="sites_start_crawling"),
    # path("sites_list_update/", views.sites_list_update, name="sites_list"),
    # path("delete/<int:pk>/", views.ContactDeleteView.as_view(), name="contacts_delete"),
    #
]
