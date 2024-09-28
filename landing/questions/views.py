from django.shortcuts import redirect, render
from django.http import JsonResponse

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
        {"form": form, "question_list": question_list, "remaining_time": remaining_time},
    )


def submit(request, question_list_id):
    from questions.models import QuestionListSubmission
    from questions.forms import QuestionListForm

    if request.method == "GET":
        return redirect("questions")

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
    correct_questions = str(float(submission.result["correct"])) + "%"
    time = (submission.finished_at - submission.created_at).total_seconds()

    return JsonResponse(
        {
            "corrects": correct_questions,
            "time": format_time(time),
        }
    )
