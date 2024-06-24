from tabnanny import verbose
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock, PageChooserBlock, RichTextBlock

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class QuestionListIndex(Page):
    parent_page_types = ["home.LandingPage"]
    is_creatable = False

    default_instructions = RichTextField(max_length=255, verbose_name="Instruções padrão", null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        context["lists"] = QuestionList.objects.live()
        return context

    content_panels = Page.content_panels + [
        FieldPanel("default_instructions"),
    ]

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

class QuestionList(Page):
    parent_page_types = ["questions.QuestionListIndex"]

    questions = StreamField(
        [
            ("question", PageChooserBlock(page_type="questions.QuestionItem")),
        ],
        null=True,
        blank=True,
    )

    duration = models.IntegerField(verbose_name="Duração em minutos", default=120)

    instructions = RichTextField(max_length=255, verbose_name="Instruções", null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("questions"),
        FieldPanel("duration"),
        FieldPanel("instructions"),
    ]

    ## define the verbose name
    class Meta:
        verbose_name = "Lista de Questões"

    @property
    def list_size(self):
        return len(self.questions)

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

class QuestionItem(Page):
    parent_page_types = ["questions.QuestionList", "questions.QuestionListIndex"]
    question = RichTextField(max_length=255, verbose_name="Enunciado da questão")
    answers = StreamField(
        [
            (
                "option", StructBlock([
                    ("answer", RichTextBlock()),
                    ("is_correct", BooleanBlock(default=False, required=False)),
                ])
            )
        ], null=True, blank=True, max_num=5, min_num=2, verbose_name="Alternativas"
    )

    content_panels = Page.content_panels + [
        FieldPanel("question"),
        FieldPanel("answers"),
    ]

    class Meta:
        verbose_name = "Questão"

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

class QuestionListSubmission(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    questionsList = models.ForeignKey("questions.QuestionList", on_delete=models.CASCADE)
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.list.title}"