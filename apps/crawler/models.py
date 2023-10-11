from django.db import models


class Site(models.Model):
    transact_id = models.UUIDField()
    url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SearchResult(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
