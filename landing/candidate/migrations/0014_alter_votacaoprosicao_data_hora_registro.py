# Generated by Django 3.2.12 on 2022-08-10 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0013_autorproposicao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votacaoprosicao',
            name='data_hora_registro',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
