# Generated by Django 4.2 on 2024-09-15 18:53

from django.db import migrations
from users.models import CustomUser


def create_supersu(apps, schema_editor):
    CustomUser.objects.filter(superuser=True).delete()
    CustomUser.objects.create_superuser(email="admin", password="admin")

def remove_supersu(apps, schema_editor):
    CustomUser.objects.filter(email="admin").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0002_create_supersu"),
    ]

    operations = [
        migrations.RunPython(create_supersu, remove_supersu),
    ]
