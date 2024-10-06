# Generated by Django 4.2 on 2024-10-06 21:22

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0004_alter_questionitemsubject_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionitem",
            name="answers",
            field=wagtail.fields.StreamField(
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
    ]
