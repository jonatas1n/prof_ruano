from django.urls import path
from .views import start, test, submit, get_submission_data

app_name = "listas"

urlpatterns = [
    path("<int:question_list_id>/", test, name="test"),
    path("<int:question_list_id>/start", start, name="start"),
    path("<int:question_list_id>/submit", submit, name="submit"),
    path("submission/<int:submission_id>/", get_submission_data, name="submission"),
]
