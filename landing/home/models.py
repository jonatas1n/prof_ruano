from wagtail.models import Page
from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock, PageChooserBlock, URLBlock
from wagtail.admin.panels import FieldPanel
from questions.models import QuestionList, QuestionListIndex

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        context["prev"] = hint_pages[context["index"] - 1] if context["index"] > 0 else None
        context["next"] = hint_pages[context["index"] + 1] if context["index"] < len(hint_pages) - 1 else None
        return context

    @method_decorator(login_required)
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)