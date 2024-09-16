from django.shortcuts import render
from questions.models import QuestionList, QuestionListSubmission

# def start_list(request, question_list_id):
#     question_list = QuestionList.objects.get(id=question_list_id)
#     submission = QuestionListSubmission.objects.create(user=request.user, questionsList=question_list, answers={})
#     return submission