# from django.shortcuts import render
import asyncio

from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView

from apps.crawler.additionaly.search_subsite_db import async_search_for_site_sub_sites_from_db
from apps.crawler.additionaly.sites_check import check_is_site_exist
from apps.crawler.additionaly.start_crawling import start_crawling
from apps.crawler.forms import SiteForm, GetSatesListForm, CreateSiteForm
from apps.crawler.models import Site

from apps.crawler.additionaly.sites_delete_all import delete_sites


class SitesListView(ListView):
    model = Site
    context_object_name = "sites_list"
    template_name = "crawler/sites_list.html"


def site_create_view(request):
    template_for_render = "crawler/site_create.html"

    if request.method == "POST":
        form = CreateSiteForm(request.POST)
        url_text = form.data["url_text"]
        if not check_is_site_exist(url_text):
            messages.add_message(request, messages.INFO, "Site is not exist. Please enter other name of site.")
        elif form.is_valid():
            site = Site.objects.filter(url=url_text).first()
            if site is None:
                Site.objects.create(url=url_text, flag_was_finished_crawling=False)
                template_for_render = "crawler/sites_list.html"
            else:
                messages.add_message(request, messages.INFO, "Site was present in db. Please enter other name of site.")

    else:
        form = CreateSiteForm()

    return render(
        request=request,
        template_name=template_for_render,
        context=dict(sites_list=Site.objects.all(), form=form),
    )


def site_edit(request, site_id):
    site = get_object_or_404(Site, pk=site_id)

    if request.method == "POST":
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            # form.user = request.user
            form.save()
            return redirect("crawler:sites_list")
    else:
        form = SiteForm(instance=site)

    return render(request, "crawler/site_edit.html", {"form": form, "site": site})


def site_delete(request, site_id):
    site = get_object_or_404(Site, pk=site_id)

    if request.method == "POST":
        site.delete()
        return redirect("crawler:sites_list")

    return render(request, "crawler/site_delete.html", {"site": site})


def delete_sites_all_view(request):
    delete_sites()
    return redirect(reverse_lazy("crawler:sites_list"))


def start_crawling_sites_all_view(request):
    asyncio.run(async_search_for_site_sub_sites_from_db())
    return redirect(reverse_lazy("crawler:sites_list"))


def get_sites_list_view(request):
    template_for_render = "crawler/get_sites_list.html"

    if request.method == "POST":
        form = GetSatesListForm(request.POST)

        if form.is_valid():
            sites_list_text = form.cleaned_data["sites_text"]
            asyncio.run(start_crawling(site_text=sites_list_text))
            template_for_render = "crawler/sites_list.html"

    else:
        form = GetSatesListForm()

    return render(
        request=request,
        template_name=template_for_render,
        context=dict(sites_list=Site.objects.all(), form=form),
    )
