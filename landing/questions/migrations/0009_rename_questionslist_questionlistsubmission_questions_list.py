# Generated by Django 4.2 on 2024-09-19 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0008_alter_questionitem_answers"),
    ]

    operations = [
        migrations.RenameField(
            model_name="questionlistsubmission",
            old_name="questionsList",
            new_name="question_list",
        ),
    ]
