from wagtail.models import Page
from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import (
    BooleanBlock,
    TextBlock,
    StructBlock,
    CharBlock,
)
from wagtail.admin.panels import FieldPanel
from questions.models import QuestionList, QuestionListIndex, QuestionListSubmission

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def get_stats(user):
    # get_time = lambda submission: submission.finished_at - submission.created_at
    get_results = lambda submission: submission.result
    def get_subjects(submission):
        subjects = []
        for question in submission.question_list.questions.all():
            subjects += [subject.name for subject in question.subjects.all()]
        subjects = list(set(subjects))
        return subjects

    submissions = QuestionListSubmission.objects.filter(user=user, is_finished=True)
    last_submissions = submissions.order_by("-finished_at")[:15]
    total = submissions.count()

    # average_time = [get_time(submission) for submission in submissions if submission]
    # average_time = sum(average_time) / len(average_time) if average_time else 0

    results = [get_results(submission) for submission in submissions]

    subjects = [get_subjects(submission) for submission in submissions]
    subjects = sum(subjects, [])
    subjects = list(set(subjects))

    return {"last_submissions": last_submissions, "total": total, "average_time": "234343242", "subjects": subjects}
class LandingPage(MetadataPageMixin, Page):
    is_creatable = False
    max_count = 1

    popup = StreamField(
        [
            (
                "popup",
                StructBlock(
                    [
                        ("active", BooleanBlock(label="Ativo", required=False)),
                        ("title", CharBlock(label="Título", required=False)),
                        ("text", TextBlock(label="Texto do popup", required=False)),
                    ],
                    max_num=1,
                    required=False,
                ),
            )
        ],
        max_num=1,
        null=True,
        blank=True,
    )

    def get_context(self, request):
        context = super().get_context(request)
        active_submission = QuestionListSubmission.get_active_submissions(request.user)
        if active_submission:
            active_list = active_submission.question_list
            context["active_list"] = active_list
        lists = QuestionList.objects.all()
        if lists:
            context["lists"] = lists
            context["lists_slug"] = QuestionListIndex.objects.first().slug
        context["stats"] = get_stats(request.user)
        context["hints"] = HintPage.objects.filter(is_active=True)
        return context

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    content_panels = Page.content_panels + [
        FieldPanel("popup"),
    ]


class HintPage(Page):
    parent_page_types = ["home.LandingPage"]

    description = RichTextField(verbose_name="Descrição")
    is_active = models.BooleanField(verbose_name="Ativo", default=True)
    link = models.URLField(verbose_name="Link", null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("is_active"),
        FieldPanel("link"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        hint_pages = HintPage.objects.filter(is_active=True)
        context["index"] = list(hint_pages).index(self)
        context["prev"] = (
            hint_pages[context["index"] - 1] if context["index"] > 0 else None
        )
        context["next"] = (
            hint_pages[context["index"] + 1]
            if context["index"] < len(hint_pages) - 1
            else None
        )
        return context

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)
