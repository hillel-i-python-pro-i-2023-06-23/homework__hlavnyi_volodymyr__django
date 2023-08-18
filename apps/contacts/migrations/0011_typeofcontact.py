# Generated by Django 4.2.4 on 2023-08-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0010_contact_date_of_birth"),
    ]

    operations = [
        migrations.CreateModel(
            name="TypeOfContact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=20, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
