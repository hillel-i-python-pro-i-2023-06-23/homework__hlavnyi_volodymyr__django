from django.db import models


class Site(models.Model):
    url = models.CharField(max_length=200)
    flag_was_finished_crawling = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubSite(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    sub_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
