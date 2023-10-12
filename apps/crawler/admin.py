from django.contrib import admin

from .models import Site, SubSite


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("url", "flag_was_finished_crawling", "created_at", "updated_at")
    list_filter = ("flag_was_finished_crawling", "created_at", "updated_at")
    search_fields = ("url", "was_finished_crawling")


@admin.register(SubSite)
class SubSiteAdmin(admin.ModelAdmin):
    list_display = ("site", "sub_url", "created_at", "updated_at")
    list_filter = ("site", "created_at", "updated_at")
    search_fields = ("site",)
