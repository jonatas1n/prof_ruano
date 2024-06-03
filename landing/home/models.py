from wagtail.core.models import Page
from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock


class LandingPage(MetadataPageMixin, Page):
    is_creatable = False

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

    content_panels = Page.content_panels + [
        StreamFieldPanel("popup"),
    ]
