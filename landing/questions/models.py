from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock, PageChooserBlock, RichTextBlock

class QuestionListIndex(Page):
    parent_page_types = ["home.LandingPage"]
    is_creatable = False

    def get_context(self, request):
        context = super().get_context(request)
        context["lists"] = QuestionList.objects.live()
        return context

class QuestionList(Page):
    parent_page_types = ["questions.QuestionListIndex"]

    questions = StreamField(
        [
            ("question", PageChooserBlock(page_type="questions.QuestionItem")),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("questions"),
    ]

class QuestionItem(Page):
    parent_page_types = ["questions.QuestionList"]
    question = RichTextField(max_length=255)
    answers = StreamField(
        [
            (
                "option", StructBlock([
                    ("answer", RichTextBlock()),
                    ("is_correct", BooleanBlock(default=False, required=False)),
                ])
            )
        ], null=True, blank=True, max_num=5, min_num=2
    )

    content_panels = Page.content_panels + [
        FieldPanel("question"),
        FieldPanel("answers"),
    ]