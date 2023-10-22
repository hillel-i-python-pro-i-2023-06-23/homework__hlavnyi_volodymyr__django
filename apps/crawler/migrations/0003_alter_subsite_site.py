# Generated by Django 4.2.6 on 2023-10-15 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("crawler", "0002_alter_site_options_alter_subsite_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subsite",
            name="site",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="sub_sites", to="crawler.site"
            ),
        ),
    ]