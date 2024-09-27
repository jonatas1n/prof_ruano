from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import BooleanBlock, StructBlock, CharBlock
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager
from modelcluster.models import ClusterableModel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.utils import timezone

from questions import views as questions_views

from datetime import timedelta
import unicodedata


class QuestionListIndex(RoutablePageMixin, Page):
    parent_page_types = ["home.LandingPage"]
    max_count = 1

    default_instructions = RichTextField(
        max_length=255,
        verbose_name="Instruções padrões para a realização dos testes",
        null=True,
        blank=True,
    )

    def get_context(self, request):
        context = super().get_context(request)
        context["lists"] = QuestionList.objects.live()
        active_submission = QuestionListSubmission.get_active_submissions(request.user)
        if active_submission:
            active_list = active_submission.questionsList
            context["active_list"] = active_list

        return context

    content_panels = Page.content_panels + [
        FieldPanel("default_instructions"),
    ]

    @method_decorator(login_required)
    @path("<int:question_list_id>/", name="test")
    def test(self, request, question_list_id):
        return questions_views.test(request, question_list_id)

    @method_decorator(login_required)
    @path("<int:question_list_id>/start", name="start")
    def start(self, request, question_list_id):
        return questions_views.start(request, question_list_id)

    @method_decorator(login_required)
    @path("<int:question_list_id>/submit", name="submit")
    def submit(self, request, question_list_id):
        return questions_views.submit(request, question_list_id)

    @method_decorator(login_required)
    @path("submission/<int:submission_id>/", name="submission")
    def get_submission_data(self, request, submission_id):
        return questions_views.get_submission_data(request, submission_id)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = "listas"
        super().save(*args, **kwargs)


class QuestionItemSubject(TaggedItemBase):
    content_object = ParentalKey(
        "QuestionItem", related_name="tagged_items", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        normalized_text = unicodedata.normalize("NFD", self.tag.name)
        self.tag.name = "".join(
            c for c in normalized_text if unicodedata.category(c) != "Mn"
        )
        super().save(*args, **kwargs)


class QuestionItem(ClusterableModel, Orderable):
    question_list = ParentalKey("questions.QuestionList", related_name="questions")
    question = RichTextField(max_length=255, verbose_name="Enunciado da questão")
    subjects = ClusterTaggableManager(through=QuestionItemSubject, blank=True)

    answers = StreamField(
        [
            (
                "option",
                StructBlock(
                    [
                        ("answer", CharBlock()),
                        ("is_correct", BooleanBlock(default=False, required=False)),
                    ]
                ),
            )
        ],
        null=True,
        blank=True,
        max_num=5,
        min_num=2,
        verbose_name="Alternativas",
    )

    panels = [
        FieldPanel("question"),
        FieldPanel("subjects"),
        FieldPanel("answers"),
    ]


class QuestionList(Page):
    parent_page_types = ["questions.QuestionListIndex"]
    duration = models.IntegerField(verbose_name="Duração em minutos", default=120)
    instructions = RichTextField(
        max_length=255, verbose_name="Instruções", null=True, blank=True
    )

    def start_list(self, request):
        existing_submissions = QuestionListSubmission.get_active_submissions(
            request.user
        )
        if existing_submissions:
            return
        submission = QuestionListSubmission.objects.create(
            user=request.user, questionsList=self, answers={}
        )
        return submission

    content_panels = Page.content_panels + [
        InlinePanel("questions", label="Questões"),
        FieldPanel("duration"),
        FieldPanel("instructions"),
    ]

    class Meta:
        verbose_name = "Lista de Questões"

    @property
    def list_size(self):
        return len(self.questions)

    def get_answers(self, answers):
        pass

    @property
    def get_instructions(self):
        if not self.instructions:
            return self.get_parent().specific.default_instructions
        return self.instructions

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        active_submission = QuestionListSubmission.get_active_submissions(request.user)
        if active_submission:
            active_list = active_submission.questionsList
            return redirect(f"/questions/{active_list.id}")
        return redirect(f"/questions/{self.id}")


class QuestionListSubmission(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    question_list = models.ForeignKey(
        "questions.QuestionList", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)

    answers = models.JSONField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)

    def is_active(self):
        duration = self.question_list.duration
        return (
            not self.is_finished
            and self.created_at + timedelta(minutes=duration) > timezone.now()
        )

    @staticmethod
    def get_active_submissions(user):
        user_submissions = QuestionListSubmission.objects.filter(
            user=user, is_finished=False
        )
        if not user_submissions:
            return None

        for user_submission in user_submissions:
            if user_submission.is_active():
                return user_submission

        return None

    def set_result(self):
        result = {"questions": [], "total": 0, "correct": 0, "incorrect": 0}

        question_list = self.question_list
        for question_item in question_list.questions.all():
            user_answer = self.answers.get(str(question_item.id))
            correct_answer = None
            for answer in question_item.answers:
                if answer.value.get("is_correct"):
                    correct_answer = answer.value.get("answer")
                    break

            is_correct = user_answer == correct_answer
            result["questions"].append(
                {
                    "id": question_item.id,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                }
            )

            result["total"] += 1
            result["correct"] += 1 if is_correct else 0
            result["incorrect"] += 1 if not is_correct else 0

        self.result = result
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.question_list.title}"
