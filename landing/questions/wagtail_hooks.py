from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.panels import FieldPanel, InlinePanel
from .models import QuestionList, QuestionItem
from taggit.models import TaggedItemBase

class QuestionItemInlinePanel(InlinePanel):
    model = QuestionItem
    panels = [
        FieldPanel("question"),
        FieldPanel("subjects"),
        FieldPanel("answers"),
    ]

class QuestionListAdmin(ModelAdmin):
    model = QuestionList
    menu_label = "Listas"
    menu_icon = "list-ul"
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ("title", "duration")
    search_fields = ("title")
    panels = [
        FieldPanel("title"),
        FieldPanel("duration"),
        FieldPanel("instructions"),
        InlinePanel("questions"),
    ]

modeladmin_register(QuestionListAdmin)
