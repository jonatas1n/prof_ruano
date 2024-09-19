from django.shortcuts import redirect, render, get_object_or_404
from questions.models import QuestionList, QuestionListSubmission, QuestionListIndex
from questions.forms import QuestionListForm


def start(request, question_list_id):
    active_submission = QuestionListSubmission.get_active_submissions(request.user)

    if active_submission:
        return redirect(
            "questions:test", question_list_id=active_submission.question_list.id
        )

    question_list = QuestionList.objects.get(pk=question_list_id)
    if request.method == "GET":
        return render(
            request,
            "questions/question_list.html",
            {"question_list": question_list},
        )

    QuestionListSubmission(user=request.user, question_list=question_list).save()

    return redirect("questions:test", question_list_id=question_list_id)


def test(request, question_list_id):
    active_submission = QuestionListSubmission.get_active_submissions(request.user)
    if not active_submission:
        return redirect("questions:start", question_list_id=question_list_id)

    if active_submission.question_list.id != int(question_list_id):
        return redirect("questions:test", question_list_id=question_list_id)

    question_list = active_submission.question_list
    questions = question_list.questions.all()
    form = QuestionListForm(questions=questions)
    return render(
        request,
        "questions/question_test.html",
        {"form": form, "question_list": question_list},
    )


def submit(request, question_list_id):
    if request.method == "GET":
        return redirect("questions")

    active_submission = QuestionListSubmission.get_active_submissions(request.user)
    if not active_submission:
        return redirect("questions:start", question_list_id=question_list_id)

    if active_submission.question_list.id != int(question_list_id):
        return redirect("questions:test", question_list_id=question_list_id)

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


def index(request):
    index_page = QuestionListIndex.objects.all().first()
    if index_page:
        return redirect(index_page.url)
    return redirect("/")
