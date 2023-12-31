# Generated by Django 4.2.5 on 2023-10-12 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("url", models.CharField(max_length=200)),
                ("flag_was_finished_crawling", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SubSite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sub_url", models.CharField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("site", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="crawler.site")),
            ],
        ),
    ]
