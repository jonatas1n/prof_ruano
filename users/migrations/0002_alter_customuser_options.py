# Generated by Django 4.2 on 2024-10-02 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"verbose_name": "Usuário", "verbose_name_plural": "Usuários"},
        ),
    ]