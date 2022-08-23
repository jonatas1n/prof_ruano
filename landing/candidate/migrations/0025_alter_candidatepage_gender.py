# Generated by Django 3.2.12 on 2022-08-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0024_alter_candidatepage_opinions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatepage',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'MASCULINO'), ('F', 'FEMININO'), ('N', 'NÃO DIVULGÁVEL')], max_length=1, null=True),
        ),
    ]
