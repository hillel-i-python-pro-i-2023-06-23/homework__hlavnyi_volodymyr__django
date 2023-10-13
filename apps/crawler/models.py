from django.db import models


class Site(models.Model):
    url = models.CharField(max_length=200)
    flag_was_finished_crawling = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def as_json(self):
        return dict(
            site_id=self.id,
            url=self.url,
            flag_was_finished_crawling=self.flag_was_finished_crawling,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
        )

    class Meta:
        ordering = ["-updated_at", "-created_at", "url"]


class SubSite(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    sub_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def as_json(self):
        return dict(
            sub_site_id=self.id,
            site=self.site.as_json(),
            sub_url=self.sub_url,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
        )

    class Meta:
        ordering = ["-updated_at", "-created_at", "site"]
