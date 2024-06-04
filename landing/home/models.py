from wagtail.models import Page
from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BooleanBlock, TextBlock, StructBlock, CharBlock, PageChooserBlock
from wagtail.admin.panels import FieldPanel
class LandingPage(MetadataPageMixin, Page):
    is_creatable = False

    menu_top = StreamField(
        [
            (
                "menu_top",
                StructBlock(
                    [
                        ("active", BooleanBlock(label="Ativo", required=False, default=True)),
                        ("title", CharBlock(label="Título", required=True)),
                        ("page", PageChooserBlock(required=True)),
                    ],
                    required=False,
                ),
            )
        ],
        max_num=2,
        null=True,
        blank=True,
    )

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
        FieldPanel("menu_top"),
        FieldPanel("popup"),
    ]
