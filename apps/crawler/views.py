# from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from apps.crawler.forms import SiteForm
from apps.crawler.models import Site


class SitesListView(ListView):
    model = Site
    context_object_name = "sites_list"
    template_name = "crawler/sites_list.html"


class SiteCreateView(CreateView):
    model = Site
    fields = ("url",)
    success_url = reverse_lazy("crawler:sites_list")
    template_name = "crawler/site_create.html"


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
