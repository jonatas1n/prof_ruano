# Generated by Django 4.2 on 2024-10-02 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0003_alter_questionitem_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="questionitemsubject",
            options={"verbose_name": "Assunto", "verbose_name_plural": "Assuntos"},
        ),
        migrations.AlterModelOptions(
            name="questionlistindex",
            options={
                "verbose_name": "Índice de Listas de Questões",
                "verbose_name_plural": "Índices de Listas",
            },
        ),
        migrations.AlterModelOptions(
            name="questionlistsubmission",
            options={
                "verbose_name": "Submissão de Lista de Questões",
                "verbose_name_plural": "Submissões de Listas de Questões",
            },
        ),
    ]