from wagtail.models import Page
from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock, PageChooserBlock, URLBlock
from wagtail.admin.panels import FieldPanel
from questions.models import QuestionList, QuestionListIndex
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
        context["lists"] = QuestionList.objects.all()
        context['lists_slug'] = QuestionListIndex.objects.first().slug
        context["hints"] = HintPage.objects.filter(is_active=True)
        return context

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