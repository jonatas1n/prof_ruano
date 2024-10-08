# Generated by Django 4.2 on 2024-09-13 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0093_uploadedfile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionItem",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "question",
                    wagtail.fields.RichTextField(
                        max_length=255, verbose_name="Enunciado da questão"
                    ),
                ),
                (
                    "answers",
                    wagtail.fields.StreamField(
                        [
                            (
                                "option",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("answer", wagtail.blocks.RichTextBlock()),
                                        (
                                            "is_correct",
                                            wagtail.blocks.BooleanBlock(
                                                default=False, required=False
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ],
                        blank=True,
                        null=True,
                        verbose_name="Alternativas",
                    ),
                ),
            ],
            options={
                "verbose_name": "Questão",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="QuestionList",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "questions",
                    wagtail.fields.StreamField(
                        [
                            (
                                "question",
                                wagtail.blocks.PageChooserBlock(
                                    page_type=["questions.QuestionItem"]
                                ),
                            )
                        ],
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    "duration",
                    models.IntegerField(default=120, verbose_name="Duração em minutos"),
                ),
                (
                    "instructions",
                    wagtail.fields.RichTextField(
                        blank=True, max_length=255, null=True, verbose_name="Instruções"
                    ),
                ),
            ],
            options={
                "verbose_name": "Lista de Questões",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="QuestionListIndex",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "default_instructions",
                    wagtail.fields.RichTextField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Instruções padrão",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="QuestionListSubmission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answers", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_finished", models.BooleanField(default=False)),
                (
                    "questionsList",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questions.questionlist",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
