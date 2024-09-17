from django.urls import path
from . import views

app_name = "questions"

urlpatterns = [
    path("<int:question_list_id>", views.test, name="test"),
    path("<int:question_list_id>/start", views.start, name="start"),
    path("<int:question_list_id>/submit", views.submit, name="submit"),
]
