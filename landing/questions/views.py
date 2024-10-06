from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from wagtail.fields import StreamValue
import json

from questions.util import format_time


def start(request, question_list_id):
    from questions.models import QuestionList, QuestionListSubmission

    active_submission = QuestionListSubmission.get_active_submissions(request.user)
    if active_submission:
        return redirect(
            "listas:test", question_list_id=active_submission.question_list.id
        )

    question_list = QuestionList.objects.get(pk=question_list_id)
    if request.method == "GET":
        return render(
            request,
            "questions/question_start.html",
            {"question_list": question_list},
        )

    QuestionListSubmission(user=request.user, question_list=question_list).save()

    return redirect("listas:test", question_list_id=question_list_id)


def test(request, question_list_id):
    from questions.models import QuestionListSubmission
    from questions.forms import QuestionListForm

    active_submission = QuestionListSubmission.get_active_submissions(request.user)
    if not active_submission:
        return redirect("listas:start", question_list_id=question_list_id)

    if active_submission.question_list.id != int(question_list_id):
        return redirect("listas:test", question_list_id=question_list_id)

    question_list = active_submission.question_list
    questions = question_list.questions.all()
    remaining_time = active_submission.get_remaining_time()
    form = QuestionListForm(questions=questions)
    return render(
        request,
        "questions/question_test.html",
        {
            "form": form,
            "question_list": question_list,
            "remaining_time": remaining_time,
        },
    )


def submit(request, question_list_id):
    from questions.models import QuestionListSubmission
    from questions.forms import QuestionListForm

    if request.method == "GET":
        return redirect("/listas")

    active_submission = QuestionListSubmission.get_active_submissions(request.user)
    if not active_submission:
        return redirect("listas:start", question_list_id=question_list_id)

    if active_submission.question_list.id != int(question_list_id):
        return redirect("listas:test", question_list_id=question_list_id)

    question_list = active_submission.question_list
    questions = question_list.questions.all()

    form = QuestionListForm(request.POST, questions=questions)
    if form.is_valid():
        form.save(active_submission.id)
        return redirect("/")

    return render(
        request,
        "questions/question_test.html",
        {"form": form, "question_list": question_list, "errors": form.errors},
    )


def get_submission_data(request, submission_id):
    from questions.models import QuestionListSubmission

    submission = QuestionListSubmission.objects.get(pk=submission_id)
    correct_questions = submission.result["correct"] * 100 / submission.result["total"]
    correct_questions = f"{correct_questions:.2f}%"
    time = (submission.finished_at - submission.created_at).total_seconds()
    subjects = submission.question_list.questions.values_list(
        "subjects__name", flat=True
    )
    subjects = list(set(subjects))

    return JsonResponse(
        {
            "corrects": correct_questions,
            "time": format_time(time),
            "subjects": subjects,
        }
    )

def import_from_json_view(request):
    from questions.forms import JsonUploadForm
    from questions.models import QuestionList, QuestionItem

    form = JsonUploadForm()

    if request.method == "POST":
            form = JsonUploadForm(request.POST, request.FILES)
            if form.is_valid():
                list_title = form.cleaned_data["list_title"]
                json_file = form.cleaned_data["json_data"]
                json_string = json_file.read().decode("utf-8")
                json_data = json.loads(json_string)

                new_list = QuestionList.objects.create(title=list_title)
                for question_data in json_data:
                    new_question_item = QuestionItem.objects.create(
                        question=question_data["question"],
                        question_list=new_list,
                    )
                    new_question_item.subjects.add(question_data["subject"])

                    answers = [
                        ("option", {"answer": answer["answer"], "is_correct": answer.get("is_correct", False)})
                        for answer in question_data["answers"]
                    ]
                    new_question_item.answers = StreamValue(new_question_item.answers.stream_block, answers)
                    new_question_item.save()

                return redirect("/admin/questions/questionlist/")
    return render(
        request,
        "wagtailadmin/json_processing.html",
        {"form": form},
    )
