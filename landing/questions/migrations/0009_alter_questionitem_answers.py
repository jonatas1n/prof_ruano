# Generated by Django 4.2 on 2024-06-04 23:18

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_alter_questionitem_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionitem',
            name='answers',
            field=wagtail.fields.StreamField([('option', wagtail.blocks.StructBlock([('answer', wagtail.blocks.RichTextBlock()), ('is_correct', wagtail.blocks.BooleanBlock(default=False))]))], blank=True, null=True),
        ),
    ]
