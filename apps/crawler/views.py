# from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from apps.crawler.additionaly.start_crawling import start_crawling
from apps.crawler.forms import SiteForm, GetSatesListForm
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


def get_sites_list_view(request):
    if request.method == "POST":
        form = GetSatesListForm(request.POST)

        if form.is_valid():
            sites_list_text = form.cleaned_data["sites_text"]
            start_crawling(site_text=sites_list_text)
            return render(
                request=request,
                template_name="crawler/sites_list.html",
                context=dict(sites_list=Site.objects.all(), form=form),
            )
    else:
        form = GetSatesListForm()
        return render(
            request=request,
            template_name="crawler/get_sites_list.html",
            context=dict(sites_list=Site.objects.all(), form=form),
        )
