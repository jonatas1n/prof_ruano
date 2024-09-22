from django import template
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
    
    last_submissions = []
    subjects = []
    total = 0

    submissions = QuestionListSubmission.objects.filter(user=user, is_finished=True).order_by("-finished_at")
    if submissions:

        submissions = sorted(submissions, key=lambda x: x.finished_at, reverse=True)
        last_submissions = submissions[:15]
        total = submissions.count()

        # average_time = [get_time(submission) for submission in submissions if submission]
        # average_time = sum(average_time) / len(average_time) if average_time else 0

        results = [get_results(submission) for submission in submissions]

        subjects = [get_subjects(submission) for submission in submissions]
        subjects = sum(subjects, [])
        subjects = list(set(subjects))

    context = {"submissions": submissions, "last_submissions": last_submissions, "total": total, "average_time": "234343242", "subjects": subjects}
    return context
