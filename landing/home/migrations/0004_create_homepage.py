# Generated by Django 3.2.25 on 2024-06-03 23:10

from django.db import migrations
import wagtail.blocks
import wagtail.fields
from home.models import LandingPage
from wagtail.models import Page

def create_homepage(apps, schema_editor):
    root_page = Page.objects.get(pk=1)
    landing_page = LandingPage(title='Site do Prof. Ruano')
    
    root_page.add_child(instance=landing_page)
    root_page.save()

def delete_homepage(apps, schema_editor):
    landing_page = LandingPage.objects.get(title='Site do Prof. Ruano')
    landing_page.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_landingpage_menu_top'),
    ]

    operations = [
        migrations.RunPython(create_homepage, delete_homepage),
    ]
