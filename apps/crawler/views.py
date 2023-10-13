# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext, loader
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from apps.crawler.additionaly.start_crawling import start_crawling
from apps.crawler.forms import SiteForm, GetSatesListForm
from apps.crawler.models import Site

from apps.crawler.additionaly.sites_delete_all import delete_sites

# import asyncio


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


def delete_sites_all_view(request):
    delete_sites()
    return redirect(reverse_lazy("crawler:sites_list"))


def sites_list_update(request):
    # query = Site.objects.all()
    sites_list = [ob.as_json() for ob in Site.objects.all()]
    # sites_list = query
    return HttpResponse(
        loader.get_template("crawler/sites_list.html").render(
            RequestContext(request, JsonResponse({"sites_list": sites_list}))
        )
    )
    # return HttpResponse(JsonResponse({'sites_list': sites_list}))
    #    return redirect("crawler:sites_list", JsonResponse({'sites_list': sites_list}))
    # render(request, "crawler/sites_list.html", {"sites_list": sites_list})
    # # import json
    # # from django.http import HttpResponse
    # ...
    # def my_ajax(request):
    #     data = {
    #         'key1': 'val1',
    #         'key2': 'val2',
    #     }
    #     return HttpResponse(json.dumps(data))


def get_sites_list_view(request):
    template_for_render = "crawler/get_sites_list.html"

    if request.method == "POST":
        form = GetSatesListForm(request.POST)

        if form.is_valid():
            sites_list_text = form.cleaned_data["sites_text"]
            # main part of Project !
            start_crawling(site_text=sites_list_text)
            template_for_render = "crawler/sites_list.html"

    else:
        form = GetSatesListForm()

    return render(
        request=request,
        template_name=template_for_render,
        context=dict(sites_list=Site.objects.all(), form=form),
    )
