# Generated by Django 5.1.6 on 2025-02-20 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_customuser_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="phone",
        ),
    ]
