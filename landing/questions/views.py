from django.shortcuts import redirect, render, get_object_or_404
from questions.models import QuestionList, QuestionListSubmission
from questions.forms import QuestionListForm


def start(request, question_list_id=None):
    active_submission = QuestionListSubmission.get_active_submissions(request.user)
    question_list = QuestionList.objects.get(pk=question_list_id)

    if active_submission and active_submission.questionsList != question_list:
        return redirect(
            "questions:test", question_list_id=active_submission.questionsList.id
        )

    if request.method == "GET":
        return render(
            request,
            "questions/question_list.html",
            {"question_list": question_list},
        )

    QuestionListSubmission(user=request.user, questionsList=question_list).save()

    return redirect("questions:test", question_list_id=question_list_id)


def test(request, question_list_id):
    question_list = get_object_or_404(QuestionList, pk=question_list_id)
    questions = question_list.questions.all()
    form = QuestionListForm(questions=questions)
    if not question_list:
        return redirect("/")
    return render(
        request,
        "questions/question_test.html",
        {"form": form, "question_list": question_list},
    )


def submit(request, question_list_id):
    if request.method == "GET":
        return redirect("home")

    question_list = get_object_or_404(QuestionList, pk=question_list_id)
    questions = question_list.questions.all()

    form = QuestionListForm(request.POST, questions=questions)
    if form.is_valid():
        submission = form.save(commit=False)
        submission.user = request.user
        submission.questionsList = question_list
        submission.save()
        return redirect("questions:start", question_list_id=question_list_id)

    return render(
        request,
        "questions/question_test.html",
        {"form": form, "question_list": question_list, "errors": form.errors},
    )
