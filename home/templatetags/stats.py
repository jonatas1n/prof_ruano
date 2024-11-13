from django import template
from questions.util import format_time
from questions.models import QuestionListSubmission

register = template.Library()


@register.inclusion_tag("home/tags/stats.html")
def stats(user):
    get_results = lambda submission: submission.result

    def get_subjects(submission):
        subjects = []
        for question in submission.question_list.questions.all():
            subjects += [subject.name for subject in question.subjects.all()]
        subjects = list(set(subjects))
        return subjects

    subjects = []
    total = 0
    average_time = None
    corrects = None

    submissions = QuestionListSubmission.objects.filter(
        user=user, is_finished=True
    ).order_by("-finished_at")
    if submissions:

        submissions = sorted(submissions, key=lambda x: x.finished_at, reverse=True)
        total = len(submissions)

        get_time = lambda submission: (
            submission.finished_at - submission.created_at
        ).total_seconds()

        average_time = [
            get_time(submission) for submission in submissions if submission
        ]
        average_time = sum(average_time) / len(average_time) if average_time else 0
        average_time = format_time(average_time)

        results = [get_results(submission) for submission in submissions]

        corrects = sum([result["correct"] for result in results if result], 0)

        total_questions = sum([result["total"] for result in results if result], 0)
        corrects = (corrects / total_questions) * 100 if total_questions else 0
        corrects = f"{corrects:.2f}%"

        subjects = [get_subjects(submission) for submission in submissions]
        subjects = sum(subjects, [])
        subjects = list(set(subjects))

    context = {
        "submissions": submissions,
        "total": total,
        "subjects": subjects,
        "average_time": average_time,
        "corrects": corrects,
    }

    return context
