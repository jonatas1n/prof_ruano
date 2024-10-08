# Generated by Django 4.2 on 2024-09-15 21:34

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0002_create_questions_list_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionlistindex",
            name="default_instructions",
            field=wagtail.fields.RichTextField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="Instruções padrões para a realização dos testes",
            ),
        ),
    ]
