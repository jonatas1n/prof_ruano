from django.db import migrations
from questions.models import QuestionListIndex
from home.models import LandingPage

class Migration(migrations.Migration):

    def create_question_list_index(apps, schema_editor):
        homepage = LandingPage.objects.all().first()
        question_list_index = QuestionListIndex(title='Lista de Perguntas')
        homepage.add_child(instance=question_list_index)
        homepage.save()

    def delete_question_list_index(apps, schema_editor):
        question_list_index = QuestionListIndex.objects.all()
        if not question_list_index:
            return
        question_list_index.first().delete()

    dependencies = [
        ('questions', '0004_questionlistindex'),
    ]

    operations = [
        migrations.RunPython(create_question_list_index, delete_question_list_index),
    ]
