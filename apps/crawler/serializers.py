from rest_framework import serializers

from apps.crawler.models import Site


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["id", "url", "flag_was_finished_crawling", "created_at", "updated_at"]


class SubSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["id", "url", "flag_was_finished_crawling", "created_at", "updated_at"]
