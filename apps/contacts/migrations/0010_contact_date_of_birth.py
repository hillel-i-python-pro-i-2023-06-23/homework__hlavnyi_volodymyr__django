# Generated by Django 4.2.4 on 2023-08-15 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0009_rename_group_of_contact_groupofcontact_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
    ]
